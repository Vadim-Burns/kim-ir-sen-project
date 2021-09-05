"""
This file contains all cryptography operations and fucntions
"""

from cryptography.fernet import Fernet

import config

security_key = config.security_key
main_fernet = Fernet(security_key.encode())


def generate_key() -> bytes:
    return Fernet.generate_key()


def encrypt_text(text: str, key: bytes) -> str:
    return Fernet(key).encrypt(
        text.encode()
    ).decode()


def encrypt_key(id: int, key: bytes) -> str:
    return main_fernet.encrypt(
        (
                str(id) + ";" + key.decode()
        ).encode()
    ).decode()


# TODO: Ошибка ввода латиницы
def decrypt_key(key: str) -> (int, str):
    key_decrypted = main_fernet.decrypt(
        key.encode()
    ).decode()

    key_info = key_decrypted.split(';')

    return int(key_info[0]), key_info[1]


def decrypt_text(encrypted_text: str, key: str) -> str:
    return Fernet(key.encode()).decrypt(
        encrypted_text.encode()
    ).decode()
