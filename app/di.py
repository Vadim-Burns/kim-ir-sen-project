import inject

from services import AbstractCryptService, CryptService
from services import AbstractKimService, KimService


def DI():
    def di_configuration(binder):
        crypt_service = CryptService()
        kim_service = KimService(crypt_service)

        binder.bind(AbstractCryptService, crypt_service)
        binder.bind(AbstractKimService, kim_service)

    inject.configure_once(di_configuration)
