from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import os
import sys
import hashlib
import gzip
import re
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto import aes_gcm
from crypto import rsa_utils
import json

import pathlib
FRONTEND_DIR = pathlib.Path(__file__).parent.parent / 'frontend'
app = Flask(__name__)
CORS(app)

# Production configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True

# --- Session-Only Audit Log (NEW) ---
audit_log = []

def log_operation(operation: str, method: str, success: bool, error_msg: str = None, details: dict = None):
    """Log encryption operation without storing plaintext."""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'operation': operation,
        'method': method,
        'success': success,
        'error': error_msg,
        'details': details or {}
    }
    audit_log.append(log_entry)
    # Keep only last 100 entries
    if len(audit_log) > 100:
        audit_log.pop(0)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password meets minimum requirements."""
    if len(password) < 8:
        return False, 'Password must be at least 8 characters (12+ recommended)'
    if len(password) < 12:
        return True, 'Consider using 12+ characters for stronger security'
    return True, 'Password strength is good'

# --- RSA Endpoints ---
@app.route('/api/generate_rsa_keys', methods=['GET'])
def generate_rsa_keys():
    priv, pub = rsa_utils.generate_key_pair()
    fingerprint = rsa_utils.compute_key_fingerprint(pub)
    log_operation('Generate RSA Keys', 'RSA', True, details={'fingerprint': fingerprint})
    return jsonify({'private_key': priv, 'public_key': pub, 'fingerprint': fingerprint})

@app.route('/api/rsa_encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext', '')
    public_key = data.get('public_key', '')
    if not plaintext or not public_key:
        log_operation('Encrypt (RSA Hybrid)', 'RSA Hybrid', False, 'Missing plaintext or public key')
        return jsonify({'error': 'Missing plaintext or public key'}), 400
    try:
        # Use fingerprinting version
        ciphertext = rsa_utils.hybrid_encrypt_with_fingerprint(plaintext.encode(), public_key)
        log_operation('Encrypt (RSA Hybrid)', 'RSA Hybrid', True, details={'size': len(plaintext)})
        return jsonify({'ciphertext': ciphertext})
    except Exception as e:
        log_operation('Encrypt (RSA Hybrid)', 'RSA Hybrid', False, str(e))
        return jsonify({'error': f'RSA encryption failed: {e}'}), 500

@app.route('/api/rsa_decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext', '')
    private_key = data.get('private_key', '')
    if not ciphertext or not private_key:
        log_operation('Decrypt (RSA Hybrid)', 'RSA Hybrid', False, 'Missing ciphertext or private key')
        return jsonify({'error': 'Missing ciphertext or private key'}), 400
    try:
        plaintext = rsa_utils.hybrid_decrypt(ciphertext, private_key)
        log_operation('Decrypt (RSA Hybrid)', 'RSA Hybrid', True, details={'size': len(plaintext)})
        return jsonify({'plaintext': plaintext.decode(errors='replace')})
    except Exception as e:
        log_operation('Decrypt (RSA Hybrid)', 'RSA Hybrid', False, str(e))
        return jsonify({'error': f'RSA decryption failed: {e}'}), 500

# --- AES-GCM Endpoints ---
@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext', '')
    password = data.get('password', '')
    profile = data.get('profile', 'balanced')  # security profile: fast, balanced, high
    
    if not plaintext or not password:
        log_operation('Encrypt (AES-GCM)', 'AES-GCM', False, 'Missing plaintext or password')
        return jsonify({'error': 'Missing plaintext or password'}), 400
    
    # Validate password strength
    is_valid, msg = validate_password_strength(password)
    if not is_valid:
        log_operation('Encrypt (AES-GCM)', 'AES-GCM', False, msg)
        return jsonify({'error': msg, 'warning': msg}), 400
    
    try:
        ciphertext = aes_gcm.encrypt(plaintext.encode(), password, profile)
        log_operation('Encrypt (AES-GCM)', 'AES-GCM', True, details={'profile': profile, 'size': len(plaintext)})
        return jsonify({'ciphertext': ciphertext})
    except Exception as e:
        log_operation('Encrypt (AES-GCM)', 'AES-GCM', False, str(e))
        return jsonify({'error': f'AES encryption failed: {e}'}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext', '')
    password = data.get('password', '')
    if not ciphertext or not password:
        log_operation('Decrypt (AES-GCM)', 'AES-GCM', False, 'Missing ciphertext or password')
        return jsonify({'error': 'Missing ciphertext or password'}), 400
    try:
        plaintext = aes_gcm.decrypt(ciphertext, password)
        log_operation('Decrypt (AES-GCM)', 'AES-GCM', True, details={'size': len(plaintext)})
        return jsonify({'plaintext': plaintext.decode(errors='replace')})
    except ValueError as e:
        # Wrong password or tampered ciphertext
        log_operation('Decrypt (AES-GCM)', 'AES-GCM', False, str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log_operation('Decrypt (AES-GCM)', 'AES-GCM', False, str(e))
        return jsonify({'error': f'AES decryption failed: {e}'}), 500

@app.route('/api/encrypt_file', methods=['POST'])
def encrypt_file():
    data = request.get_json()
    filedata_b64 = data.get('filedata_b64')
    password = data.get('password', '')
    if not filedata_b64 or not password:
        return jsonify({'error': 'Missing file data or password'}), 400
    try:
        file_bytes = base64.b64decode(filedata_b64)
        ciphertext = aes_gcm.encrypt(file_bytes, password)
        return jsonify({'ciphertext': ciphertext})
    except Exception as e:
        return jsonify({'error': f'File encryption failed: {e}'}), 500

@app.route('/api/decrypt_file', methods=['POST'])
def decrypt_file():
    data = request.get_json()
    ciphertext = data.get('ciphertext')
    password = data.get('password', '')
    filename = data.get('filename', 'decrypted')
    if not ciphertext or not password:
        return jsonify({'error': 'Missing ciphertext or password'}), 400
    try:
        plainfile = aes_gcm.decrypt(ciphertext, password)
        # Return as list of ints for JS to handle
        return jsonify({'plainfile': list(plainfile), 'filename': filename.replace('.enc', '')})
    except Exception as e:
        return jsonify({'error': f'File decryption failed: {e}'}), 500


# --- NEW: Password Strength Validation ---
@app.route('/api/check_password_strength', methods=['POST'])
def check_password_strength():
    """Validate password against security criteria."""
    data = request.get_json()
    password = data.get('password', '')
    if not password:
        return jsonify({'strength': 0, 'feedback': 'Password required'}), 400
    
    score = 0
    feedback = []
    
    if len(password) >= 12:
        score += 30
    elif len(password) >= 8:
        score += 15
    else:
        feedback.append('Use at least 8 characters (12+ recommended)')
    
    if re.search(r'[a-z]', password):
        score += 10
    else:
        feedback.append('Add lowercase letters')
    
    if re.search(r'[A-Z]', password):
        score += 10
    else:
        feedback.append('Add uppercase letters')
    
    if re.search(r'[0-9]', password):
        score += 15
    else:
        feedback.append('Add numbers')
    
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        score += 25
    else:
        feedback.append('Add special characters')
    
    strength_label = 'Weak' if score < 30 else 'Fair' if score < 60 else 'Good' if score < 80 else 'Strong'
    
    return jsonify({
        'strength': min(100, score),
        'label': strength_label,
        'feedback': feedback
    })


# --- NEW: File Integrity Check (SHA-256) ---
@app.route('/api/verify_file_hash', methods=['POST'])
def verify_file_hash():
    """Verify file integrity using SHA-256 hash."""
    data = request.get_json()
    filedata_b64 = data.get('filedata_b64')
    expected_hash = data.get('expected_hash')
    
    if not filedata_b64:
        return jsonify({'error': 'Missing file data'}), 400
    
    try:
        file_bytes = base64.b64decode(filedata_b64)
        computed_hash = hashlib.sha256(file_bytes).hexdigest()
        
        match = computed_hash == expected_hash if expected_hash else None
        return jsonify({
            'hash': computed_hash,
            'match': match,
            'message': 'File integrity verified' if match else 'File hash mismatch' if match is False else 'File hash computed'
        })
    except Exception as e:
        return jsonify({'error': f'Hash verification failed: {e}'}), 500


# --- NEW: Compression before Encryption ---
@app.route('/api/compress_data', methods=['POST'])
def compress_data():
    """Compress data using gzip before encryption."""
    data = request.get_json()
    plaintext = data.get('plaintext', '')
    
    if not plaintext:
        return jsonify({'error': 'Missing plaintext'}), 400
    
    try:
        plaintext_bytes = plaintext.encode() if isinstance(plaintext, str) else plaintext
        compressed = gzip.compress(plaintext_bytes, compresslevel=9)
        compressed_b64 = base64.b64encode(compressed).decode()
        reduction = ((len(plaintext_bytes) - len(compressed)) / len(plaintext_bytes) * 100) if plaintext_bytes else 0
        
        return jsonify({
            'original_size': len(plaintext_bytes),
            'compressed_size': len(compressed),
            'compression_ratio': f'{reduction:.1f}%',
            'data': compressed_b64
        })
    except Exception as e:
        return jsonify({'error': f'Compression failed: {e}'}), 500


# --- NEW: Decompress Data ---
@app.route('/api/decompress_data', methods=['POST'])
def decompress_data():
    """Decompress gzip-compressed data."""
    data = request.get_json()
    compressed_b64 = data.get('data')
    
    if not compressed_b64:
        return jsonify({'error': 'Missing compressed data'}), 400
    
    try:
        compressed = base64.b64decode(compressed_b64)
        decompressed = gzip.decompress(compressed)
        
        return jsonify({
            'plaintext': decompressed.decode(errors='replace'),
            'size': len(decompressed)
        })
    except Exception as e:
        return jsonify({'error': f'Decompression failed: {e}'}), 500


# --- NEW: RSA Digital Signature ---
@app.route('/api/rsa_sign', methods=['POST'])
def rsa_sign():
    """Sign data with RSA private key."""
    data = request.get_json()
    message = data.get('message', '')
    private_key = data.get('private_key', '')
    
    if not message or not private_key:
        return jsonify({'error': 'Missing message or private key'}), 400
    
    try:
        signature = rsa_utils.sign_message(message, private_key)
        return jsonify({'signature': signature})
    except Exception as e:
        return jsonify({'error': f'Signing failed: {e}'}), 500


# --- NEW: RSA Signature Verification ---
@app.route('/api/rsa_verify', methods=['POST'])
def rsa_verify():
    """Verify RSA signature with public key."""
    data = request.get_json()
    message = data.get('message', '')
    signature = data.get('signature', '')
    public_key = data.get('public_key', '')
    
    if not message or not signature or not public_key:
        return jsonify({'error': 'Missing message, signature, or public key'}), 400
    
    try:
        is_valid = rsa_utils.verify_signature(message, signature, public_key)
        return jsonify({
            'valid': is_valid,
            'message': 'Signature verified' if is_valid else 'Signature verification failed'
        })
    except Exception as e:
        return jsonify({'error': f'Verification failed: {e}'}), 500


# --- NEW: Encryption with Metadata ---
@app.route('/api/encrypt_with_metadata', methods=['POST'])
def encrypt_with_metadata():
    """Encrypt data with timestamp and description metadata."""
    data = request.get_json()
    plaintext = data.get('plaintext', '')
    password = data.get('password', '')
    description = data.get('description', '')
    
    if not plaintext or not password:
        return jsonify({'error': 'Missing plaintext or password'}), 400
    
    try:
        # Add metadata
        metadata = {
            'timestamp': datetime.utcnow().isoformat(),
            'description': description,
            'size': len(plaintext)
        }
        
        # Create payload with metadata
        payload = {
            'metadata': metadata,
            'data': plaintext
        }
        import json
        payload_str = json.dumps(payload)
        
        ciphertext = aes_gcm.encrypt(payload_str.encode(), password)
        return jsonify({
            'ciphertext': ciphertext,
            'timestamp': metadata['timestamp']
        })
    except Exception as e:
        return jsonify({'error': f'Encryption with metadata failed: {e}'}), 500


# --- NEW: Decrypt with Metadata Extraction ---
@app.route('/api/decrypt_with_metadata', methods=['POST'])
def decrypt_with_metadata():
    """Decrypt data and extract metadata."""
    data = request.get_json()
    ciphertext = data.get('ciphertext', '')
    password = data.get('password', '')
    
    if not ciphertext or not password:
        return jsonify({'error': 'Missing ciphertext or password'}), 400
    
    try:
        plaintext_bytes = aes_gcm.decrypt(ciphertext, password)
        payload = json.loads(plaintext_bytes.decode())
        
        return jsonify({
            'plaintext': payload.get('data', ''),
            'metadata': payload.get('metadata', {}),
            'success': True
        })
    except json.JSONDecodeError:
        return jsonify({'error': 'Decrypted data is not valid metadata format'}), 400
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {e}'}), 500




# Serve frontend at root
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'clean_encryption_app.html')

# Serve static files (css, js, etc.) if needed
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# --- NEW: Audit Log Endpoint ---
@app.route('/api/audit_log', methods=['GET'])
def get_audit_log():
    """Return session audit log (no plaintext, no passwords)."""
    return jsonify({'log': audit_log})

# --- NEW: Session Status ---
@app.route('/api/session_status', methods=['GET'])
def session_status():
    """Return session info (operations count, last operation, etc.)."""
    return jsonify({
        'operations_count': len(audit_log),
        'last_operation': audit_log[-1] if audit_log else None,
        'session_start': 'Session initiated'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])

