import unittest
import json
from backend.app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_encrypt_decrypt_text(self):
        password = 'apitestpass'
        plaintext = 'API test message'
        # Encrypt
        resp = self.client.post('/api/encrypt', json={'plaintext': plaintext, 'password': password})
        self.assertEqual(resp.status_code, 200)
        ciphertext = resp.get_json()['ciphertext']
        # Decrypt
        resp2 = self.client.post('/api/decrypt', json={'ciphertext': ciphertext, 'password': password})
        self.assertEqual(resp2.status_code, 200)
        decrypted = resp2.get_json()['plaintext']
        self.assertEqual(decrypted, plaintext)

    def test_encrypt_decrypt_file(self):
        password = 'apifilepass'
        filedata = [i % 256 for i in range(256)]
        # Encrypt
        resp = self.client.post('/api/encrypt_file', json={'filename': 'file.bin', 'filedata': filedata, 'password': password})
        self.assertEqual(resp.status_code, 200)
        ciphertext = resp.get_json()['ciphertext']
        # Decrypt
        resp2 = self.client.post('/api/decrypt_file', json={'filename': 'file.bin.enc', 'filedata': [ord(c) for c in ciphertext], 'password': password})
        # Note: This test expects the API to handle filedata as bytes correctly
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('plainfile', resp2.get_json())

if __name__ == '__main__':
    unittest.main()
