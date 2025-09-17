import os
import base64
import json
from typing import Tuple, Dict
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

PBKDF2_ITERATIONS = 200_000
SALT_SIZE = 16  # bytes
NONCE_SIZE = 12  # bytes
KEY_SIZE = 32  # 256 bits


def derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode())


def encrypt(plaintext: bytes, password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    metadata = {
        'alg': 'AES-GCM',
        'salt': base64.b64encode(salt).decode(),
        'nonce': base64.b64encode(nonce).decode(),
        'iterations': PBKDF2_ITERATIONS,
    }
    out = {
        'metadata': metadata,
        'ciphertext': base64.b64encode(ciphertext).decode(),
    }
    return base64.b64encode(json.dumps(out).encode()).decode()


def decrypt(encoded: str, password: str) -> bytes:
    out = json.loads(base64.b64decode(encoded).decode())
    metadata = out['metadata']
    salt = base64.b64decode(metadata['salt'])
    nonce = base64.b64decode(metadata['nonce'])
    iterations = metadata.get('iterations', PBKDF2_ITERATIONS)
    key = derive_key(password, salt, iterations)
    aesgcm = AESGCM(key)
    ciphertext = base64.b64decode(out['ciphertext'])
    return aesgcm.decrypt(nonce, ciphertext, None)
