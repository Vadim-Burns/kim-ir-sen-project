from flask import Flask
from random import randint
import os
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)
security_key = os.environ.get("SECURITY_KEY")


def _generate_key(length=32):
    """
    This functions generates key.
    :param `int` length:
    :return `str` main_key:
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!#$%&*+=-/\\"
    main_key = ""
    for _ in range(length):
        main_key += alphabet[randint(0, len(alphabet) - 1)]
    return main_key


def _get_fermet_key(key):
    salt = b"zo=6bLX1$SKMA$ZK+Kvhuf6yo\ZGy#&C"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(key.encode()))


def _encrypt_text(key, text):
    f = Fernet(_get_fermet_key(key))
    return f.encrypt(text.encode()).decode()


def _decrypt_text(key, text):
    f = Fernet(_get_fermet_key(key))
    return f.decrypt(text.encode()).decode()


@app.route('/')
def hello_world():
    return security_key

