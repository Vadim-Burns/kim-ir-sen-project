from flask import Flask
from random import randint
import os

app = Flask(__name__)
security_key = os.environ.get("SECURITY_KEY")


def _generate_key(length=32):
    """
    This functions generates main key. Main key is used to encrypt note key and note id to one string
    :param `int` length:
    :return `str` main_key:
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!#$%&*+=-/\\"
    main_key = ""
    for _ in range(length):
        main_key += alphabet[randint(0, len(alphabet) - 1)]
    return main_key

def _encrypt_text(text):
    pass

@app.route('/')
def hello_world():
    return security_key


if __name__ == '__main__':
    app.run()
