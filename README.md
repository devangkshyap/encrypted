# Secure Encryption & Decryption App v2.0

## 🎯 Overview
A professional-grade web application for secure encryption, decryption, and cryptographic operations. Features modern AES-GCM encryption, RSA hybrid encryption, digital signatures, and file integrity verification.

**Perfect for:**
- Protecting sensitive documents
- Secure file sharing
- Digital signature verification
- Data integrity checking
- Learning cryptography best practices

## ✨ Features

### Core Encryption
- ✅ **AES-GCM** (256-bit) - Fast, secure, authenticated encryption
- ✅ **RSA Hybrid** - 2048-bit RSA + AES-GCM for key sharing
- ✅ **Password-based** - PBKDF2 with 200,000 iterations
- ✅ **File support** - Encrypt/decrypt any file type
- ✅ **Metadata** - Automatic timestamps and descriptions

### NEW in v2.0 🚀
- ✅ **Digital Signatures** - RSA-PSS sign and verify messages
- ✅ **File Hashing** - SHA-256 integrity verification
- ✅ **Password Strength** - Real-time validation + server-side check
- ✅ **Data Compression** - Gzip compression before encryption
- ✅ **Metadata Encryption** - Track when/what was encrypted
- ✅ **Signature Verification** - Prove authenticity and non-repudiation

## 🔐 Security Features
- **Authenticated Encryption**: AES-GCM prevents tampering
- **Strong Key Derivation**: PBKDF2 with salt (200,000 iterations)
- **Random Nonces**: Fresh nonce for every encryption
- **RSA-PSS Signatures**: Industry-standard padding
- **No Key Storage**: Keys never persisted
- **Client-Side**: Most operations happen in browser

## 📁 Project Structure
```
.
├── backend/
│   └── app.py                 # Flask API with 10+ endpoints
├── crypto/
│   ├── aes_gcm.py             # AES-256-GCM encryption
│   └── rsa_utils.py           # RSA + Hybrid encryption + Signatures
├── frontend/
│   ├── clean_encryption_app.html  # Modern UI (blue/cyan theme)
│   └── assets/
├── docs/
│   ├── new_features.md        # Complete feature documentation
│   ├── api_usage.md
│   ├── encryption_process.md
│   └── threat_model.md
├── tests/
│   ├── test_api.py
│   └── test_crypto.py
├── QUICKSTART.md              # Quick reference guide
├── IMPLEMENTATION_NOTES.md    # Technical details
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Flask & Flask-CORS
- cryptography library

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Start backend server
python backend/app.py

# Open browser to http://localhost:5000
```

### Usage Examples

**Encrypt Text:**
1. Select "AES-GCM (Password)" method
2. Enter text to encrypt
3. Enter a strong password (12+ characters recommended)
4. Click "Encrypt"
5. Copy the encrypted output

**Sign a Message:**
1. Go to "Digital Signatures" section
2. Generate RSA keys or paste existing ones
3. Enter message to sign
4. Click "Sign with Private Key"
5. Share message + signature with recipient

**Verify File Integrity:**
1. Select file
2. Click "Compute Hash"
3. SHA-256 hash appears
4. Recipient verifies their file hash matches

## 📊 API Endpoints

### Encryption
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/encrypt` | POST | Encrypt text with password (AES-GCM) |
| `/api/decrypt` | POST | Decrypt text with password |
| `/api/encrypt_file` | POST | Encrypt file |
| `/api/decrypt_file` | POST | Decrypt file |

### RSA/Hybrid
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/generate_rsa_keys` | GET | Generate RSA key pair (2048-bit) |
| `/api/rsa_encrypt` | POST | Encrypt with RSA public key |
| `/api/rsa_decrypt` | POST | Decrypt with RSA private key |
| `/api/rsa_sign` | POST | Sign message with private key |
| `/api/rsa_verify` | POST | Verify signature with public key |

### Utilities
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/verify_file_hash` | POST | Compute SHA-256 hash |
| `/api/compress_data` | POST | Compress with gzip |
| `/api/decompress_data` | POST | Decompress gzip data |
| `/api/check_password_strength` | POST | Validate password strength |
| `/api/encrypt_with_metadata` | POST | Encrypt + timestamp |
| `/api/decrypt_with_metadata` | POST | Decrypt + extract metadata |

## 🔑 Cryptographic Details

### Algorithms
- **Encryption**: AES-256-GCM (NIST FIPS 197)
- **Key Derivation**: PBKDF2-SHA256 (200,000 iterations)
- **Asymmetric**: RSA-2048 with OAEP padding
- **Signatures**: RSA-PSS with SHA-256 (PKCS#3.1)
- **Hashing**: SHA-256 (FIPS 180-4)
- **Compression**: gzip with level 9

### Parameters
| Parameter | Value | Reason |
|-----------|-------|--------|
| PBKDF2 Iterations | 200,000 | OWASP 2023 recommendation |
| Salt Size | 16 bytes | Sufficient entropy |
| Nonce Size | 12 bytes | GCM standard |
| Key Size | 256 bits | AES-256 |
| RSA Modulus | 2048 bits | Minimum recommended |

## 🛡️ Security Recommendations

### Do's ✅
- Use 12+ character passwords
- Store private keys securely (offline)
- Verify signatures before trusting data
- Check file hashes after transfer
- Use HTTPS in production
- Backup keys in secure location
- Change passwords periodically

### Don'ts ❌
- Don't share private keys
- Don't use simple passwords
- Don't reuse nonces (app handles this)
- Don't trust unverified signatures
- Don't skip integrity checks
- Don't backup keys on same device
- Don't leave keys in browser cache

## 📚 Documentation

- **QUICKSTART.md** - Quick reference for all features
- **IMPLEMENTATION_NOTES.md** - Technical implementation details
- **docs/new_features.md** - Comprehensive API documentation
- **docs/encryption_process.md** - How encryption works
- **docs/threat_model.md** - Security analysis

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Test specific module
python -m pytest tests/test_crypto.py -v
```

## 📊 Performance

- **Encryption**: ~10 MB/sec (typical)
- **Decryption**: ~10 MB/sec (typical)
- **Signature**: ~10-50ms per operation
- **Hash**: ~1-5ms per MB
- **Compression**: ~10-100ms for typical documents

## 🎨 UI Features

- **Modern Design**: Blue/cyan gradient theme
- **Dark Mode**: Toggle with 🌙 button
- **Responsive**: Works on desktop and mobile
- **Accessibility**: WCAG 2.1 compliant
- **Real-time Feedback**: Notifications for all operations
- **Session History**: Track encryption operations

## 🔄 Version History

### v2.0 (Current) - December 2025
- ✨ Added digital signatures (RSA-PSS)
- ✨ Added file integrity verification (SHA-256)
- ✨ Added server-side password validation
- ✨ Added data compression (gzip)
- ✨ Added metadata encryption
- 🎨 Redesigned UI with blue/cyan theme
- 📚 Complete API documentation

### v1.0 - Initial Release
- Basic AES-GCM encryption
- RSA hybrid encryption
- File encryption/decryption
- Web UI
- PBKDF2 key derivation

## 🤝 Contributing

Pull requests welcome! Please ensure:
- All tests pass
- Code follows existing style
- Security best practices maintained
- Documentation updated

## 📜 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This application uses standard cryptographic libraries but is provided "as-is" without guarantee. For production use with sensitive data, conduct security audits and threat modeling appropriate to your use case. The developers are not liable for any misuse or security breaches.

## 📞 Support

- 📖 Read documentation in `docs/` directory
- 🐛 Report issues on GitHub
- 💬 Check QUICKSTART.md for common questions

---

**Made with 🔐 security and ❤️ care**

