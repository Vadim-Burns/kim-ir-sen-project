import inject

from repositories import AbstractNoteRepo, NoteRepo
from services import AbstractCryptService, CryptService
from services import AbstractKimService, KimService


def DI():
    def di_configuration(binder):
        crypt_service = CryptService()
        note_repo = NoteRepo()
        kim_service = KimService(crypt_service, note_repo)

        binder.bind(AbstractCryptService, crypt_service)
        binder.bind(AbstractNoteRepo, note_repo)
        binder.bind(AbstractKimService, kim_service)

    inject.configure_once(di_configuration)
