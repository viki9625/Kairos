from cryptography.fernet import Fernet
from core.config import settings


# settings.fernet_key must be a 32 url-safe base64-encoded key
fernet = Fernet(settings.fernet_key.encode())


def encrypt_text(plaintext: str) -> str:
    return fernet.encrypt(plaintext.encode()).decode()


def decrypt_text(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()