"""
This file contains all cryptography operations and fucntions
"""

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

import config

security_key = config.security_key
main_fernet = Fernet(security_key.encode())


def generate_key() -> str:
    return Fernet.generate_key().decode()


def encrypt_text(text: str, key: str) -> str:
    return Fernet(key.encode()).encrypt(
        text.encode()
    ).decode()


def encrypt_key(id: int, key: str) -> str:
    return main_fernet.encrypt(
        (
                str(id) + ";" + key
        ).encode()
    ).decode()


def decrypt_key(key: str) -> (int, str):
    try:
        key_decrypted = main_fernet.decrypt(
            key.encode()
        ).decode()

        key_info = key_decrypted.split(';')

        return int(key_info[0]), key_info[1]

    except InvalidToken:
        return None, None


def decrypt_text(encrypted_text: str, key: str) -> str:
    return Fernet(key.encode()).decrypt(
        encrypted_text.encode()
    ).decode()
