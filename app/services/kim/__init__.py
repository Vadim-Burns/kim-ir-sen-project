import abc
from services import AbstractCryptService
import db

class AbstractKimService(abc.ABC):

    @abc.abstractmethod
    def save_note(self, text: str) -> str:
        """
        Saving encrypted note to database, returns key
        @:param text
        """
        ...

    @abc.abstractmethod
    def get_note(self, key: str) -> str:
        """
        Getting note from database and deleting it, if no note in db returns None
        @:param key
        """
        ...


class KimService(AbstractKimService):

    def __init__(self, crypt_service: AbstractCryptService):
        self._crypt_service = crypt_service

    def save_note(self, text: str) -> str:
        key = self._crypt_service.generate_key()

        note_id = db.Note.create(
            text=self._crypt_service.encrypt_text(
                text=text,
                key=key
            )
        )

        return self._crypt_service.encrypt_key(
            id=note_id,
            key=key
        )

    def get_note(self, encrypted_key: str) -> str:
        note_id, key = self._crypt_service.decrypt_key(encrypted_key)
        if note_id is None:
            return None

        encrypted_text = db.Note.get_text_by_id(note_id)
        if encrypted_text is None:
            return None

        return self._crypt_service.decrypt_text(
            encrypted_text=encrypted_text,
            key=key
        )
