from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, base64, json

RSA_KEY_SIZE = 2048
AES_KEY_SIZE = 32
NONCE_SIZE = 12

# --- RSA Key Generation ---
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=RSA_KEY_SIZE
    )
    public_key = private_key.public_key()
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return priv_pem.decode(), pub_pem.decode()

# --- Hybrid Encrypt (RSA+AES) ---
def hybrid_encrypt(plaintext: bytes, public_pem: str) -> str:
    public_key = serialization.load_pem_public_key(public_pem.encode())
    aes_key = os.urandom(AES_KEY_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    enc_key = public_key.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    out = {
        'alg': 'RSA+AES-GCM',
        'nonce': base64.b64encode(nonce).decode(),
        'enc_key': base64.b64encode(enc_key).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode(),
    }
    return base64.b64encode(json.dumps(out).encode()).decode()

# --- Hybrid Decrypt (RSA+AES) ---
def hybrid_decrypt(encoded: str, private_pem: str) -> bytes:
    out = json.loads(base64.b64decode(encoded).decode())
    private_key = serialization.load_pem_private_key(private_pem.encode(), password=None)
    nonce = base64.b64decode(out['nonce'])
    enc_key = base64.b64decode(out['enc_key'])
    aes_key = private_key.decrypt(
        enc_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    ciphertext = base64.b64decode(out['ciphertext'])
    aesgcm = AESGCM(aes_key)
    return aesgcm.decrypt(nonce, ciphertext, None)
