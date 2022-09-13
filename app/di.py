import inject

from services import AbstractCryptService, CryptService


def DI():
    def di_configuration(binder):
        binder.bind(AbstractCryptService, CryptService())

    inject.configure_once(di_configuration)
