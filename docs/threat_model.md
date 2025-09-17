# Threat Model

## Security Goals
- Confidentiality: Only users with the correct password can decrypt data.
- Integrity: AES-GCM ensures ciphertext cannot be modified undetected.
- Usability: Simple UI, no cryptographic knowledge required.

## Assumptions
- The backend server is trusted and not compromised.
- Users choose strong, unique passwords.
- The app is served over HTTPS in production.

## Threats & Mitigations
- **Weak Passwords**: Mitigated by recommending strong passwords and using PBKDF2 with high iteration count.
- **Nonce Reuse**: Mitigated by generating a new random nonce for every encryption.
- **Man-in-the-Middle**: Mitigated by requiring HTTPS for deployment.
- **Code Injection**: No user input is executed; all crypto is handled by standard libraries.
- **Data Loss**: Users are responsible for saving their encrypted files and passwords securely.

## Out of Scope
- Server compromise, browser malware, or OS-level attacks.
- Password recovery if lost.
