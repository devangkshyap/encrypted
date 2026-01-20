import os
import base64
import json
import hmac
import hashlib
from typing import Tuple, Dict
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Versioning and security profiles
VERSION = '1.0'
PBKDF2_ITERATIONS_FAST = 100_000
PBKDF2_ITERATIONS_BALANCED = 200_000
PBKDF2_ITERATIONS_HIGH = 400_000
PBKDF2_ITERATIONS = PBKDF2_ITERATIONS_BALANCED  # default

SALT_SIZE = 16  # bytes
NONCE_SIZE = 12  # bytes
KEY_SIZE = 32  # 256 bits


def derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    """Derive encryption key from password using PBKDF2-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode())


def compute_password_hmac(password: str, salt: bytes) -> str:
    """Compute HMAC-SHA256 of password for verification without storing plaintext."""
    hmac_obj = hmac.new(salt, password.encode(), hashlib.sha256)
    return base64.b64encode(hmac_obj.digest()).decode()


def encrypt(plaintext: bytes, password: str, profile: str = 'balanced') -> str:
    """Encrypt plaintext with AES-GCM using password-derived key.
    
    Args:
        plaintext: Data to encrypt
        password: User password (min 8 chars recommended 12+)
        profile: Security profile ('fast', 'balanced', 'high')
    
    Returns:
        Base64-encoded envelope with metadata, nonce, and ciphertext
    """
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters')
    
    # Select KDF iterations based on profile
    profile_map = {'fast': PBKDF2_ITERATIONS_FAST, 'balanced': PBKDF2_ITERATIONS_BALANCED, 'high': PBKDF2_ITERATIONS_HIGH}
    iterations = profile_map.get(profile, PBKDF2_ITERATIONS_BALANCED)
    
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt, iterations)
    
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    
    # Compute password HMAC for verification
    password_hmac = compute_password_hmac(password, salt)
    
    metadata = {
        'version': VERSION,
        'alg': 'AES-GCM',
        'kdf': 'PBKDF2-SHA256',
        'profile': profile,
        'salt': base64.b64encode(salt).decode(),
        'nonce': base64.b64encode(nonce).decode(),
        'iterations': iterations,
        'password_hmac': password_hmac,  # For tamper detection
    }
    
    out = {
        'metadata': metadata,
        'ciphertext': base64.b64encode(ciphertext).decode(),
    }
    
    return base64.b64encode(json.dumps(out).encode()).decode()


def decrypt(encoded: str, password: str) -> bytes:
    """Decrypt AES-GCM ciphertext using password.
    
    Args:
        encoded: Base64-encoded envelope from encrypt()
        password: User password
    
    Returns:
        Decrypted plaintext bytes
    
    Raises:
        ValueError: If password is wrong, ciphertext is tampered, or version incompatible
    """
    try:
        out = json.loads(base64.b64decode(encoded).decode())
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError('Invalid or corrupted ciphertext envelope') from e
    
    metadata = out.get('metadata', {})
    version = metadata.get('version', '1.0')
    
    if version != VERSION:
        raise ValueError(f'Unsupported ciphertext version: {version}')
    
    salt = base64.b64decode(metadata['salt'])
    nonce = base64.b64decode(metadata['nonce'])
    iterations = metadata.get('iterations', PBKDF2_ITERATIONS)
    stored_hmac = metadata.get('password_hmac', '')
    
    # Verify password HMAC (detects wrong password)
    computed_hmac = compute_password_hmac(password, salt)
    if not hmac.compare_digest(computed_hmac, stored_hmac):
        raise ValueError('Wrong password or corrupted envelope')
    
    key = derive_key(password, salt, iterations)
    
    try:
        aesgcm = AESGCM(key)
        ciphertext = base64.b64decode(out['ciphertext'])
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext
    except Exception as e:
        raise ValueError('Decryption failed: ciphertext may be corrupted or tampered') from e
