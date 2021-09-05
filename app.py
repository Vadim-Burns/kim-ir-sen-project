"""
This file contains flask server for processing requests
"""

from flask import Flask
from flask import request, abort, render_template

import config
import crypt
import db

app = Flask(__name__, static_folder=config.static_folder)


@app.route('/')
def index():
    return app.send_static_file('index.html')


# TODO: написать описание почему два метода доступно и чем они различаются
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return app.send_static_file('create.html')
    else:
        text = request.form.get("text")
        if text is None:
            return abort(400)

        key = crypt.generate_key()

        id = db.Note.create(
            text=crypt.encrypt_text(
                text,
                key
            )
        ).id

        return render_template(
            'code.html',
            code=crypt.encrypt_key(
                id,
                key
            )
        )


@app.route("/find", methods=['POST'])
def find():
    super_key = request.form.get("key")
    if super_key is None:
        return 400

    note_id, key = crypt.decrypt_key(super_key)

    encrypted_text = db.Note.get_text_by_id(note_id)
    # TODO: поправить проверку
    if encrypted_text is None:
        return abort(404)

    return render_template(
        "note.html",
        text=crypt.decrypt_text(
            encrypted_text,
            key
        )
    )


@app.route('/api/add', methods=["POST"])
def add():
    """
    This function checks if json_data is valid, then generate random key and save
    encrypted text to database. Then generates access code for user note.id + "=" + key for text.

    Example correct answer:
    {"key": "gAAAAABhNQGGRwrwHkwydWFZfnt0N4gq"}

    Error answers:

    code - 400
    reason - json data is not valid

    """
    json_data = request.get_json()
    if json_data is None or json_data.get("text") is None:
        # TODO: удалить abort
        abort(400)

    key = crypt.generate_key()

    id = db.Note.create(
        text=crypt.encrypt_text(
            json_data.get("text"),
            key
        )
    ).id

    return {
        "key": crypt.encrypt_key(
            id,
            key
        )
    }


@app.route('/api/get', methods=["POST"])
def get():
    """
    This function checks if json_data is valid, then decrypt user access code and get id of Note.
    After that it decrypts text from note and sends back to user.

    Example correct answer:
    {"text": "hello there"}

    Error answers:

    code - 400
    reason - json data is not valid

    code - 404
    reason - note not found

    code - 404
    reason - wrong key
    """
    json_data = request.get_json()
    if json_data is None or json_data.get("key") is None:
        abort(400)

    try:

        note_id, key = crypt.decrypt_key(json_data.get("key"))

        encrypted_text = db.Note.get_text_by_id(note_id)
        if encrypted_text is None:
            return abort(404)

        return {
            "text": crypt.decrypt_text(
                encrypted_text,
                key
            )
        }
    except:
        return {"error": "Wrong key"}, 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
