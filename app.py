from flask import Flask
from random import randint
import os
import pyaes
import base64
import db
from flask import request, abort

app = Flask(__name__)
# Must be 32 byte length
security_key = os.environ.get("SECURITY_KEY")
print(security_key)


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


def _encrypt_text(key, text):
    """
    Key must be 32 byte length!!
    :param `str` key:
    :param `str` text:
    :return `str`:
    """
    aes = pyaes.AESModeOfOperationCTR(key.encode())
    ciphertext = aes.encrypt(text)
    return base64.b64encode(ciphertext).decode()


def _decrypt_text(key, text):
    """
    Key must be 32 byte length!!
    :param `str` key:
    :param `str` text:
    :return `str`:
    """
    aes = pyaes.AESModeOfOperationCTR(key.encode())
    return aes.decrypt(base64.b64decode(text.encode())).decode()


@app.route('/')
def hello_world():
    return security_key


@app.route('/api/add', methods=["POST"])
def add():
    """
    This function checks if json_data is valid, then generate random key and save
    encrypted text to database. Then generates access code for user note.id + "=" + key for text.
    """
    json_data = request.get_json()
    if json_data is None or json_data.get("text") is None:
        abort(400)

    key = _generate_key()
    encrypted_text = _encrypt_text(key, json_data.get("text"))
    id = db.Note.create(text=encrypted_text).id

    super_key = _encrypt_text(security_key, str(id) + "=" + key)
    return {"key": super_key}


@app.route('/api/get', methods=["POST"])
def get():
    """
    This function checks if json_data is valid, then decrypt user access code and get id of Note.
    After that it decrypts text from note and sends back to user.
    """
    json_data = request.get_json()
    if json_data is None or json_data.get("key") is None:
        abort(400)

    try:
        super_key_decrypted = _decrypt_text(security_key, json_data.get("key"))

        index = super_key_decrypted.find("=")
        id = int(super_key_decrypted[:index])
        key = super_key_decrypted[index + 1:]

        encrypted_text = db.Note.get_text_by_id(id)
        text = _decrypt_text(key, encrypted_text)

        return {"text": text}
    except:
        return {"error": "Wrong key"}, 404


if __name__ == '__main__':
    app.run()
