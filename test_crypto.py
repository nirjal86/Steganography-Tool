import unittest
from crypto import generate_key, encrypt_message, decrypt_message

class TestCrypto(unittest.TestCase):
    def test_encryption_decryption(self):
        key = generate_key()
        original_message = "Hello, Steganography!"
        encrypted = encrypt_message(original_message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(original_message, decrypted)

if __name__ == '__main__':
    unittest.main()
