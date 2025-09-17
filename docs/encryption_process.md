# Encryption Process

## Overview
This app uses AES-GCM (256-bit) for symmetric encryption. Keys are derived from user passwords using PBKDF2 with SHA-256, a random salt, and 200,000 iterations. All cryptographic operations use the Python `cryptography` library.

## Steps
1. **Key Derivation**: A random 16-byte salt is generated. The password and salt are used with PBKDF2 (SHA-256, 200,000 iterations) to derive a 256-bit key.
2. **Encryption**: A random 12-byte nonce is generated. AES-GCM encrypts the plaintext using the derived key and nonce, producing ciphertext and an authentication tag.
3. **Output Packaging**: The salt, nonce, ciphertext, and metadata (algorithm, iterations) are Base64-encoded and bundled for output.
4. **Decryption**: The process is reversed using the password, salt, and nonce to recover the original plaintext.

## Security Notes
- Never reuse a nonce with the same key.
- Passwords are never stored or transmitted.
- Only standard, proven cryptographic libraries are used.
