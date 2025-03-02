from cryptography.fernet import Fernet

def generate_key() -> bytes:
    """Generates a new encryption key."""
    return Fernet.generate_key()

def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypts the message using the provided key."""
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(token: bytes, key: bytes) -> str:
    """Decrypts the encrypted token using the provided key."""
    f = Fernet(key)
    return f.decrypt(token).decode()
