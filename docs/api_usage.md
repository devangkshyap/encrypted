# API Usage

## Endpoints
- `POST /api/encrypt` — Encrypt text
- `POST /api/decrypt` — Decrypt text
- `POST /api/encrypt_file` — Encrypt file
- `POST /api/decrypt_file` — Decrypt file

## Request/Response Examples
### Encrypt Text
Request: `{ "plaintext": "hello", "password": "mypassword" }`
Response: `{ "ciphertext": "..." }`

### Decrypt Text
Request: `{ "ciphertext": "...", "password": "mypassword" }`
Response: `{ "plaintext": "hello" }`

### Encrypt File
Request: `{ "filename": "file.txt", "filedata": [byte array], "password": "mypassword" }`
Response: `{ "ciphertext": "..." }`

### Decrypt File
Request: `{ "filename": "file.txt.enc", "filedata": [byte array], "password": "mypassword" }`
Response: `{ "plainfile": [byte array], "filename": "file.txt" }`
