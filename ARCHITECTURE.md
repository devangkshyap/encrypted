# 🎨 Feature Architecture & Data Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SECURE ENCRYPTION APP v2.0              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   FRONTEND (HTML/CSS/JS)            │   │
│  │                                                      │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │  Encryption Section    │  Signatures        │   │   │
│  │  │  - AES-GCM             │  - Sign Message    │   │   │
│  │  │  - RSA Hybrid          │  - Verify Sig      │   │   │
│  │  │  - File Upload         │                    │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │                                                      │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │  Tools Section         │  Admin Panel      │   │   │
│  │  │  - File Hash (SHA256)  │  - Dark Mode      │   │   │
│  │  │  - Compression         │  - Clear History  │   │   │
│  │  │  - Metadata            │                   │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │                                                      │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │  Real-time Feedback                        │   │   │
│  │  │  - Password Strength Meter                 │   │   │
│  │  │  - Notifications (Success/Error)           │   │   │
│  │  │  - Operation History Timeline              │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│           ↓              HTTP/REST API              ↑        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              BACKEND (Flask Python)                  │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────┐    │   │
│  │  │  ENCRYPTION ENDPOINTS                     │    │   │
│  │  │  ├─ /api/encrypt (AES-GCM)               │    │   │
│  │  │  ├─ /api/decrypt                         │    │   │
│  │  │  ├─ /api/encrypt_file                    │    │   │
│  │  │  ├─ /api/decrypt_file                    │    │   │
│  │  │  ├─ /api/encrypt_with_metadata           │    │   │
│  │  │  └─ /api/decrypt_with_metadata           │    │   │
│  │  └────────────────────────────────────────────┘    │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────┐    │   │
│  │  │  RSA ENDPOINTS                             │    │   │
│  │  │  ├─ /api/generate_rsa_keys               │    │   │
│  │  │  ├─ /api/rsa_encrypt (Hybrid)            │    │   │
│  │  │  ├─ /api/rsa_decrypt (Hybrid)            │    │   │
│  │  │  ├─ /api/rsa_sign                        │    │   │
│  │  │  └─ /api/rsa_verify                      │    │   │
│  │  └────────────────────────────────────────────┘    │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────┐    │   │
│  │  │  UTILITY ENDPOINTS (NEW)                  │    │   │
│  │  │  ├─ /api/check_password_strength         │    │   │
│  │  │  ├─ /api/verify_file_hash (SHA-256)      │    │   │
│  │  │  ├─ /api/compress_data                   │    │   │
│  │  │  └─ /api/decompress_data                 │    │   │
│  │  └────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│           ↓              Import                        ↑     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         CRYPTOGRAPHY LIBRARY (Python)               │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────┐    │   │
│  │  │  crypto/aes_gcm.py                         │    │   │
│  │  │  ├─ encrypt()      → AES-256-GCM           │    │   │
│  │  │  ├─ decrypt()      → AES-256-GCM           │    │   │
│  │  │  ├─ derive_key()   → PBKDF2-SHA256        │    │   │
│  │  └────────────────────────────────────────────┘    │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────┐    │   │
│  │  │  crypto/rsa_utils.py                       │    │   │
│  │  │  ├─ generate_key_pair()                   │    │   │
│  │  │  ├─ hybrid_encrypt()                      │    │   │
│  │  │  ├─ hybrid_decrypt()                      │    │   │
│  │  │  ├─ sign_message()      ← NEW             │    │   │
│  │  │  └─ verify_signature()  ← NEW             │    │   │
│  │  └────────────────────────────────────────────┘    │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────┐    │   │
│  │  │  Standard Libraries                        │    │   │
│  │  │  ├─ hashlib (SHA-256)                     │    │   │
│  │  │  ├─ gzip (compression)                    │    │   │
│  │  │  └─ json (metadata)                       │    │   │
│  │  └────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Encryption Data Flow

```
TEXT ENCRYPTION (AES-GCM)
═══════════════════════════════════════

Input:
  Plaintext (string)
  Password (string)
       ↓
  [PBKDF2-SHA256]
  200,000 iterations
  Random 16-byte salt
       ↓
  Derived Key (256-bit)
       ↓
  Random 12-byte nonce
       ↓
  [AES-256-GCM]
  Encryption + Authentication
       ↓
  Metadata JSON:
  {
    "alg": "AES-GCM",
    "salt": base64,
    "nonce": base64,
    "iterations": 200000
  }
       ↓
  Combined Package (JSON):
  {
    "metadata": {...},
    "ciphertext": base64
  }
       ↓
  [Base64 Encode]
       ↓
Output:
  Ciphertext (safe for transmission)


RSA HYBRID ENCRYPTION
═══════════════════════════════════════

Input:
  Plaintext (text)
  Public Key (PEM format, 2048-bit)
       ↓
  Generate random 256-bit AES key
       ↓
  Random 12-byte nonce
       ↓
  [AES-256-GCM] encrypt plaintext
       ↓
  [RSA-2048-OAEP] encrypt AES key
  (OAEP padding + SHA-256)
       ↓
  Package:
  {
    "alg": "RSA+AES-GCM",
    "nonce": base64,
    "enc_key": base64(encrypted),
    "ciphertext": base64
  }
       ↓
  [Base64 Encode]
       ↓
Output:
  Hybrid Ciphertext


DIGITAL SIGNATURE WORKFLOW
═══════════════════════════════════════

SIGNING:
  Input: Message, Private Key (2048-bit)
       ↓
  Message → [UTF-8 Encode]
       ↓
  [RSA-PSS] Sign with Private Key
  Algorithm: SHA-256
  Padding: PSS (maximum salt length)
       ↓
  [Base64 Encode]
       ↓
  Output: Signature (safe for transmission)


VERIFICATION:
  Input: Message, Signature, Public Key
       ↓
  [Base64 Decode] signature
       ↓
  [RSA-PSS] Verify
  Message matches signature?
       ↓
  Output: ✓ Valid or ✗ Invalid
```

---

## File Hashing Flow

```
FILE INTEGRITY VERIFICATION (SHA-256)
═════════════════════════════════════════

HASHING:
  Input: File (any format)
       ↓
  Read file as binary
       ↓
  [SHA-256 Hash Algorithm]
  Cryptographic hash function
       ↓
  Output: 64-character hex string
  Example: a3f5c... (256 bits in hex)


VERIFICATION:
  Sender:
    Original File → [SHA-256] → Hash123ABC
                                    ↓
                              Send: Hash + File
                                    
  Receiver:
    Downloaded File → [SHA-256] → Hash123ABC
                                      ↓
    Compare: Received Hash vs Computed Hash
                                      ↓
    Result: ✓ Match = Integrity OK
            ✗ Mismatch = File tampered!
```

---

## Password Strength Validation

```
PASSWORD STRENGTH SCORING
═════════════════════════════════════

Input: Password
  ↓
Check Length:
  ├─ < 8 chars? → Score = 0
  ├─ 8-11 chars? → Score += 15
  └─ 12+ chars? → Score += 30
  ↓
Check Character Types:
  ├─ Has lowercase [a-z]? → Score += 10
  ├─ Has uppercase [A-Z]? → Score += 10
  ├─ Has numbers [0-9]? → Score += 15
  └─ Has special chars? → Score += 25
  ↓
Calculate Total Score (0-100)
  ↓
Assign Label:
  ├─ 0-30: Weak
  ├─ 31-60: Fair
  ├─ 61-80: Good
  └─ 81-100: Strong
  ↓
Provide Feedback:
  ├─ Missing lowercase? → "Add lowercase"
  ├─ Missing uppercase? → "Add uppercase"
  ├─ Missing numbers? → "Add numbers"
  └─ Missing special? → "Add special chars"
  ↓
Output:
  {
    "strength": 85,
    "label": "Strong",
    "feedback": ["Use 12+ characters"]
  }
```

---

## Data Compression Pipeline

```
COMPRESSION WITH GZIP
═════════════════════════════════════

Input:
  Plaintext (large text/document)
       ↓
  [UTF-8 Encode] to bytes
       ↓
  [GZIP Compression Level 9]
  Maximum compression ratio
       ↓
  Compressed data (smaller)
       ↓
  [Base64 Encode] for transport
       ↓
Output:
  {
    "original_size": 1048576,     # 1 MB
    "compressed_size": 209715,    # 200 KB
    "compression_ratio": "80.0%",
    "data": "H4sICOpfZWYC..."
  }


DECOMPRESSION
═════════════════════════════════════

Input:
  Compressed data (Base64)
       ↓
  [Base64 Decode]
       ↓
  [GZIP Decompress]
       ↓
  Original plaintext
       ↓
Output:
  Restored original data
```

---

## Metadata Encryption Flow

```
ENCRYPTION WITH METADATA
═════════════════════════════════════

Input:
  Plaintext: "Secret data"
  Password: "MyPassword123!"
  Description: "Financial Records"
       ↓
  Build metadata object:
  {
    "timestamp": "2025-12-17T10:30:45Z",
    "description": "Financial Records",
    "size": 11
  }
       ↓
  Combine into package:
  {
    "metadata": {...},
    "data": "Secret data"
  }
       ↓
  [JSON Serialize]
       ↓
  [AES-256-GCM Encrypt]
  With PBKDF2 key derivation
       ↓
  Output:
  {
    "ciphertext": "base64_encoded",
    "timestamp": "2025-12-17T10:30:45Z"
  }


DECRYPTION WITH METADATA EXTRACTION
═════════════════════════════════════

Input:
  Ciphertext (Base64)
  Password: "MyPassword123!"
       ↓
  [AES-256-GCM Decrypt]
       ↓
  [JSON Parse]
       ↓
  Extract components:
  - plaintext: "Secret data"
  - metadata:
    * timestamp: "2025-12-17T10:30:45Z"
    * description: "Financial Records"
    * size: 11
       ↓
Output:
  {
    "plaintext": "Secret data",
    "metadata": {
      "timestamp": "...",
      "description": "...",
      "size": 11
    }
  }
```

---

## API Request/Response Flow

```
TYPICAL API CALL SEQUENCE
═════════════════════════════════════

Frontend (Browser):
  1. User enters data (text/file)
  2. Selects method (AES/RSA)
  3. Enters password/key
  4. Clicks "Encrypt"
       ↓ HTTP POST
  
Backend (Flask):
  5. Receives JSON request
  6. Validates inputs
  7. Performs encryption
  8. Packages response
       ↓ HTTP Response (JSON)

Frontend (Browser):
  9. Receives encrypted result
  10. Updates UI output
  11. Shows notification
  12. Adds to history


ERROR HANDLING FLOW
═════════════════════════════════════

User Action (e.g., encrypt)
       ↓
Input Validation:
  ├─ Empty input? → "Enter text"
  ├─ No password? → "Enter password"
  └─ Invalid key? → "Invalid key format"
       ↓
Try Encryption:
  ├─ Success → Return ciphertext
  └─ Failure → Catch exception
       ↓
Format Error Response:
  {
    "error": "Specific error message"
  }
       ↓
Frontend:
  ├─ Show error notification
  ├─ Keep input for correction
  └─ Suggest next step
```

---

## Security Model

```
THREAT & MITIGATION MATRIX
═════════════════════════════════════

THREAT                          │ MITIGATION
────────────────────────────────┼──────────────────────────
Weak password                   │ Password strength validator
                                │ Min requirements enforced
────────────────────────────────┼──────────────────────────
Nonce reuse                      │ Random nonce per encryption
                                │ Never reused
────────────────────────────────┼──────────────────────────
Tampering with ciphertext       │ AES-GCM authentication tag
                                │ Detects any modification
────────────────────────────────┼──────────────────────────
Man-in-the-middle attack        │ Use HTTPS in production
                                │ Certificate pinning (optional)
────────────────────────────────┼──────────────────────────
Forged signatures               │ RSA-2048 + PSS padding
                                │ Only private key holder can sign
────────────────────────────────┼──────────────────────────
File tampering                  │ SHA-256 file hashing
                                │ Hash comparison
────────────────────────────────┼──────────────────────────
Weak key derivation             │ PBKDF2, 200,000 iterations
                                │ 16-byte random salt
────────────────────────────────┼──────────────────────────
Brute force on key              │ Time-based rate limiting (optional)
                                │ Key stretching (PBKDF2)
────────────────────────────────┼──────────────────────────
Metadata leakage                │ Metadata encrypted with ciphertext
                                │ Visible only to authorized user
```

---

## Component Interaction Diagram

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ User Input
       │
       ↓
┌──────────────────────────────────┐
│  HTML/CSS/JS Interface           │
│  - Form inputs                   │
│  - Real-time validation          │
│  - Strength meters               │
│  - Notifications                 │
└──────┬───────────────────────────┘
       │ HTTP/REST API
       │
       ↓
┌──────────────────────────────────┐
│  Flask Backend                   │
│  - Request routing               │
│  - Input validation              │
│  - Business logic                │
└──────┬───────────────────────────┘
       │ Import
       │
       ↓
┌──────────────────────────────────┐
│  Crypto Library                  │
│  - aes_gcm module                │
│  - rsa_utils module              │
│  - Standard library              │
└──────────────────────────────────┘
       │ Delegates to
       │
       ├──→ PBKDF2-SHA256 (key derivation)
       ├──→ AES-256-GCM (encryption)
       ├──→ RSA-2048 (asymmetric)
       ├──→ RSA-PSS (signatures)
       ├──→ SHA-256 (hashing)
       └──→ gzip (compression)
```

---

**Version: 2.0** | **Complete Architecture Documentation**
