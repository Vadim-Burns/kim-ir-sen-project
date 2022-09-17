import abc
from services import AbstractCryptService


class AbstractKimService(abc.ABC):
    """
    Saving encrypted note to database
    @:param text
    @:return key
    """

    @abc.abstractmethod
    def save_note(self, text: str) -> str:
        ...

    """
    Getting note from database and deleting it
    @:param key
    @:return note
    """

    @abc.abstractmethod
    def get_note(self, key: str) -> str:
        ...


class KimService(AbstractKimService):

    def __init__(self, crypt_service: AbstractCryptService):
        self._crypt_service = crypt_service

    def save_note(self, text: str) -> str:
        return ""

    def get_note(self, key: str) -> str:
        return ""
