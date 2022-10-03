import abc

from entities import NoteEntity
from repositories.database import AbstractNoteRepo
from services import AbstractCryptService


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

    def __init__(self, crypt_service: AbstractCryptService, note_repo: AbstractNoteRepo):
        self._crypt_service = crypt_service
        self._note_repo = note_repo

    def save_note(self, text: str) -> str:
        key = self._crypt_service.generate_key()

        note = NoteEntity(
            text=self._crypt_service.encrypt_text(text, key)
        )
        note_id = self._note_repo.save_instances(instances=[note])[0].id

        return self._crypt_service.encrypt_key(
            id=note_id,
            key=key
        )

    def get_note(self, encrypted_key: str) -> str:
        note_id, key = self._crypt_service.decrypt_key(encrypted_key)
        if note_id is None:
            return None

        note = self._note_repo.get(id=note_id)
        if note is None:
            return None

        return self._crypt_service.decrypt_text(
            encrypted_text=note.text,
            key=key
        )
