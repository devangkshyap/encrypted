from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'crypto')))
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto import aes_gcm
from crypto import rsa_utils

import pathlib
FRONTEND_DIR = pathlib.Path(__file__).parent.parent / 'frontend'
app = Flask(__name__)
CORS(app)

# --- RSA Endpoints ---
@app.route('/api/generate_rsa_keys', methods=['GET'])
def generate_rsa_keys():
    priv, pub = rsa_utils.generate_key_pair()
    return jsonify({'private_key': priv, 'public_key': pub})

@app.route('/api/rsa_encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext', '')
    public_key = data.get('public_key', '')
    if not plaintext or not public_key:
        return jsonify({'error': 'Missing plaintext or public key'}), 400
    try:
        ciphertext = rsa_utils.hybrid_encrypt(plaintext.encode(), public_key)
        return jsonify({'ciphertext': ciphertext})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa_decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext', '')
    private_key = data.get('private_key', '')
    if not ciphertext or not private_key:
        return jsonify({'error': 'Missing ciphertext or private key'}), 400
    try:
        plaintext = rsa_utils.hybrid_decrypt(ciphertext, private_key)
        return jsonify({'plaintext': plaintext.decode(errors='replace')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app = Flask(__name__)
CORS(app)

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext', '')
    password = data.get('password', '')
    if not plaintext or not password:
        return jsonify({'error': 'Missing plaintext or password'}), 400
    try:
        ciphertext = aes_gcm.encrypt(plaintext.encode(), password)
        return jsonify({'ciphertext': ciphertext})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext', '')
    password = data.get('password', '')
    if not ciphertext or not password:
        return jsonify({'error': 'Missing ciphertext or password'}), 400
    try:
        plaintext = aes_gcm.decrypt(ciphertext, password)
        return jsonify({'plaintext': plaintext.decode(errors='replace')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/encrypt_file', methods=['POST'])
def encrypt_file():
    data = request.get_json()
    filedata = data.get('filedata')
    password = data.get('password', '')
    filename = data.get('filename', 'file')
    if filedata is None or not password:
        return jsonify({'error': 'Missing file or password'}), 400
    try:
        file_bytes = bytes(filedata)
        ciphertext = aes_gcm.encrypt(file_bytes, password)
        return jsonify({'ciphertext': ciphertext})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt_file', methods=['POST'])
def decrypt_file():
    data = request.get_json()
    filedata = data.get('filedata')
    password = data.get('password', '')
    filename = data.get('filename', 'decrypted')
    if filedata is None or not password:
        return jsonify({'error': 'Missing file or password'}), 400
    try:
        file_bytes = bytes(filedata)
        plainfile = aes_gcm.decrypt(file_bytes.decode(), password)
        # Return as list of ints for JS
        return jsonify({'plainfile': list(plainfile), 'filename': filename.replace('.enc', '')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Serve frontend at root
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'clean_encryption_app.html')

# Serve static files (css, js, etc.) if needed
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
