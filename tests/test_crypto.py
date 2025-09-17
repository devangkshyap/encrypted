import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto import aes_gcm

class TestAESCrypto(unittest.TestCase):
    def test_encrypt_decrypt_text(self):
        password = 'testpassword123'
        plaintext = b'Hello, world!'
        ciphertext = aes_gcm.encrypt(plaintext, password)
        decrypted = aes_gcm.decrypt(ciphertext, password)
        self.assertEqual(decrypted, plaintext)

    def test_encrypt_decrypt_file(self):
        password = 'filepass456'
        filedata = os.urandom(1024)  # 1KB random data
        ciphertext = aes_gcm.encrypt(filedata, password)
        decrypted = aes_gcm.decrypt(ciphertext, password)
        self.assertEqual(decrypted, filedata)

    def test_wrong_password(self):
        password = 'rightpass'
        wrong = 'wrongpass'
        plaintext = b'Secret'
        ciphertext = aes_gcm.encrypt(plaintext, password)
        with self.assertRaises(Exception):
            aes_gcm.decrypt(ciphertext, wrong)

if __name__ == '__main__':
    unittest.main()
