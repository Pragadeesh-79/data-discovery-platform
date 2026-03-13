from cryptography.fernet import Fernet
import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class DataEncryptor:
    def __init__(self):
        # In a real scenario, an environment variable or secure vault should provide the key.
        # For this prototype, we generate a consistent key based on a static master password.
        password = b"DPDPA-Secure-Master-Password"
        salt = b"DPDPA-salt-random-123"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.fernet = Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext sensitive data"""
        if not plaintext:
            return plaintext
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt encrypted sensitive data"""
        if not ciphertext:
            return ciphertext
        try:
            return self.fernet.decrypt(ciphertext.encode()).decode()
        except Exception:
            return "Decryption Error"

encryptor = DataEncryptor()
