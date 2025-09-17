# Secure Encryption & Decryption App

## Overview
A web app for secure encryption and decryption of text and files using AES-GCM (256-bit) with password-based key derivation (PBKDF2). Includes a simple web UI, file support, and strong security best practices.

## Features
- Encrypt/decrypt text and files
- AES-GCM (256-bit) symmetric encryption
- Key derived from password using PBKDF2 (200,000+ iterations, salt)
- Encrypted output includes salt, nonce, ciphertext, and metadata (Base64-encoded)
- Simple web UI (Encrypt/Decrypt buttons)
- Save/load encrypted files
- Security best practices (no nonce reuse, authenticated encryption)

## Project Structure
- `frontend/` – HTML/JS UI
- `backend/` – Flask API
- `crypto/` – Crypto utilities (AES-GCM, PBKDF2)
- `tests/` – Unit tests
- `docs/` – Documentation & threat model

## Usage
1. Start the backend Flask server.
2. Open the frontend in your browser.
3. Enter text or select a file, provide a password, and encrypt/decrypt.

## Security Notes
- Never reuse nonces with the same key.
- Passwords are never stored.
- Only standard, proven crypto libraries are used.

## License
MIT
