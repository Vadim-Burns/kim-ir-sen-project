from flask import Flask
from random import randint
import os
import pyaes
import base64
import db
from flask import request, abort, render_template

app = Flask(__name__, static_folder=os.path.join(os.getcwd() + "/static"))
print(app.static_folder)
# Must be 32 byte length
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
def index():
    return app.send_static_file('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return app.send_static_file('create.html')
    else:
        text = request.form.get("text")
        if text is None:
            return 400

        key = _generate_key()
        encrypted_text = _encrypt_text(key, text)
        id = db.Note.create(text=encrypted_text).id
        super_key = _encrypt_text(security_key, str(id) + "=" + key)
        return render_template('code.html', code=super_key)


@app.route("/find", methods=['POST'])
def find():
    super_key = request.form.get("key")
    if super_key is None:
        return 400

    super_key_decrypted = _decrypt_text(security_key, super_key)

    index = super_key_decrypted.find("=")
    id = int(super_key_decrypted[:index])
    key = super_key_decrypted[index + 1:]

    encrypted_text = db.Note.get_text_by_id(id)
    if encrypted_text is None:
        return 404

    text = _decrypt_text(key, encrypted_text)

    return render_template("note.html", text=text)


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
