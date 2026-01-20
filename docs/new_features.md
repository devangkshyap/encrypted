# New Features - Encryption App v2.0

## Overview
The Secure Encryption Suite has been enhanced with powerful new cryptographic capabilities for professional-grade security operations.

---

## 🔐 New Features

### 1. **Digital Signatures (RSA)**
Sign and verify messages using RSA-PSS with SHA-256.

**Use Cases:**
- Prove authenticity of messages
- Non-repudiation (sender cannot deny sending)
- Verify data integrity and origin

**API Endpoints:**
- `POST /api/rsa_sign` - Sign a message
- `POST /api/rsa_verify` - Verify a signature

**Example:**
```bash
# Sign a message
curl -X POST http://localhost:5000/api/rsa_sign \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Important document",
    "private_key": "-----BEGIN PRIVATE KEY-----\n..."
  }'

# Verify signature
curl -X POST http://localhost:5000/api/rsa_verify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Important document",
    "signature": "base64_encoded_signature",
    "public_key": "-----BEGIN PUBLIC KEY-----\n..."
  }'
```

---

### 2. **File Integrity Verification (SHA-256)**
Compute and verify file hashes to detect tampering.

**Use Cases:**
- Verify files weren't modified during transfer
- Confirm downloaded files match originals
- Detect corrupted or malicious modifications

**API Endpoint:**
- `POST /api/verify_file_hash` - Compute SHA-256 hash

**Example:**
```bash
curl -X POST http://localhost:5000/api/verify_file_hash \
  -H "Content-Type: application/json" \
  -d '{
    "filedata_b64": "base64_encoded_file_data",
    "expected_hash": "optional_hash_to_verify_against"
  }'
```

---

### 3. **Server-Side Password Strength Validation**
Validate passwords against cryptographic best practices.

**Use Cases:**
- Server-side validation of password quality
- Client-side strength indicator feedback
- Compliance with security policies

**API Endpoint:**
- `POST /api/check_password_strength` - Validate password

**Response Includes:**
- Strength score (0-100)
- Strength label (Weak/Fair/Good/Strong)
- Specific feedback for improvement

**Example:**
```bash
curl -X POST http://localhost:5000/api/check_password_strength \
  -H "Content-Type: application/json" \
  -d '{"password": "MyP@ssw0rd123!"}'
```

**Response:**
```json
{
  "strength": 95,
  "label": "Strong",
  "feedback": []
}
```

---

### 4. **Data Compression**
Compress data before encryption to reduce size.

**Use Cases:**
- Reduce ciphertext size
- Faster transmission
- Lower bandwidth usage

**API Endpoints:**
- `POST /api/compress_data` - Compress data with gzip
- `POST /api/decompress_data` - Decompress gzip data

**Response Includes:**
- Original and compressed sizes
- Compression ratio percentage
- Compressed data in Base64

**Example:**
```bash
# Compress
curl -X POST http://localhost:5000/api/compress_data \
  -H "Content-Type: application/json" \
  -d '{"plaintext": "your text here..."}'

# Decompress
curl -X POST http://localhost:5000/api/decompress_data \
  -H "Content-Type: application/json" \
  -d '{"data": "base64_compressed_data"}'
```

---

### 5. **Encryption with Metadata**
Attach metadata (timestamp, description) to encrypted data.

**Use Cases:**
- Track when data was encrypted
- Add context/description to encrypted content
- Automatic timestamping

**API Endpoints:**
- `POST /api/encrypt_with_metadata` - Encrypt with metadata
- `POST /api/decrypt_with_metadata` - Decrypt and extract metadata

**Metadata Included:**
- ISO 8601 timestamp
- User description
- Original plaintext size

**Example:**
```bash
# Encrypt with metadata
curl -X POST http://localhost:5000/api/encrypt_with_metadata \
  -H "Content-Type: application/json" \
  -d '{
    "plaintext": "Secret data",
    "password": "MyPassword123!",
    "description": "Financial Records Q4"
  }'

# Response includes timestamp
{
  "ciphertext": "base64_ciphertext",
  "timestamp": "2025-12-17T10:30:45.123456"
}
```

When decrypted:
```json
{
  "plaintext": "Secret data",
  "metadata": {
    "timestamp": "2025-12-17T10:30:45.123456",
    "description": "Financial Records Q4",
    "size": 11
  }
}
```

---

## 🎯 Use Case Examples

### Scenario 1: Secure Document Transfer
1. Use AES-GCM to encrypt a sensitive document
2. Compute file hash for verification
3. Send both ciphertext and hash to recipient
4. Recipient decrypts and verifies hash matches

### Scenario 2: Message Authentication
1. Sign important message with private key
2. Send message + signature to recipient
3. Recipient verifies signature with your public key
4. Recipient knows message is authentic and unchanged

### Scenario 3: Large File Encryption
1. Compress file using compression API
2. Encrypt compressed file with AES-GCM + password
3. Send much smaller ciphertext
4. Recipient decrypts and decompresses

### Scenario 4: Audit Trail
1. Encrypt with metadata (automatic timestamp)
2. Keep history of what/when was encrypted
3. Metadata visible only to those with password
4. Provides non-repudiation evidence

---

## 🔧 Technical Details

### Cryptographic Algorithms
- **Encryption**: AES-256-GCM (NIST approved)
- **RSA**: 2048-bit RSA-OAEP with SHA-256
- **Signatures**: RSA-PSS with SHA-256 (PKCS#3.1)
- **Hashing**: SHA-256 (FIPS 180-4)
- **Compression**: gzip (RFC 1952)

### Security Parameters
- **PBKDF2 Iterations**: 200,000 (OWASP recommendation)
- **Salt Size**: 16 bytes (128 bits)
- **Nonce Size**: 12 bytes (96 bits)
- **Key Size**: 256 bits (AES-256)

---

## ⚙️ Integration Guide

### Frontend
All new features available in UI tabs/sections:
- Digital Signatures section for signing/verifying
- Additional Tools section for hash/compression
- Password strength feedback integrated

### Backend Python API
Add to your application:
```python
# Signing
from crypto.rsa_utils import sign_message, verify_signature

signature = sign_message(message, private_key_pem)
is_valid = verify_signature(message, signature, public_key_pem)

# Compression
from backend.app import compress_data, decompress_data

# Password validation
from backend.app import check_password_strength
```

---

## 🚀 Performance Notes

- **Compression**: Best for text/JSON; minimal for already-compressed formats
- **Signature Verification**: ~10-50ms per verification
- **File Hashing**: ~1-5ms per MB of data
- **Encryption**: Scales with data size; ~10MB/sec typical

---

## 📋 API Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Missing required parameters |
| 500 | Server-side encryption/decryption error |

---

## 🛡️ Security Recommendations

1. **Always use HTTPS** in production
2. **Never** share private keys
3. **Use strong passwords** (12+ characters recommended)
4. **Verify signatures** before trusting data
5. **Check file hashes** after transfer
6. **Store encrypted data** securely
7. **Backup private keys** offline in secure location

---

## 📚 References

- [NIST SP 800-38D (GCM)](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf)
- [RFC 2898 (PBKDF2)](https://tools.ietf.org/html/rfc2898)
- [RFC 8017 (PKCS#1 RSA)](https://tools.ietf.org/html/rfc8017)
- [Python cryptography library](https://cryptography.io)
