import abc
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

import config


class AbstractCryptService(abc.ABC):

    @abc.abstractmethod
    def generate_key(self) -> str:
        ...

    @abc.abstractmethod
    def encrypt_text(self, text: str, key: str) -> str:
        ...

    @abc.abstractmethod
    def encrypt_key(self, id: int, key: str) -> str:
        ...

    @abc.abstractmethod
    def decrypt_key(self, key: str) -> (int, str):
        ...

    @abc.abstractmethod
    def decrypt_text(self, encrypted_text: str, key: str) -> str:
        ...


class CryptService(AbstractCryptService):

    def __init__(self):
        self._fernet = Fernet(config.SECURITY_KEY.encode())

    def generate_key(self) -> str:
        return Fernet.generate_key().decode()

    def encrypt_text(self, text: str, key: str) -> str:
        return Fernet(key.encode()).encrypt(
            text.encode()
        ).decode()

    def encrypt_key(self, id: int, key: str) -> str:
        return self._fernet.encrypt(
            (
                    str(id) + ";" + key
            ).encode()
        ).decode()

    def decrypt_key(self, key: str) -> (int, str):
        """
        Returns None, None if key is invalid
        """
        try:
            key_decrypted = self._fernet.decrypt(
                key.encode()
            ).decode()

            key_info = key_decrypted.split(';')

            return int(key_info[0]), key_info[1]

        except InvalidToken:
            return None, None

    def decrypt_text(self, encrypted_text: str, key: str) -> str:
        return Fernet(key.encode()).decrypt(
            encrypted_text.encode()
        ).decode()

