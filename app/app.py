"""
This file contains flask server for processing requests
"""

from flask import Flask
from flask import request, render_template, redirect

import config
import crypt
import db

app = Flask(__name__, static_folder=config.static_folder)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.errorhandler(404)
def error_404(error):
    return redirect("/")


@app.route('/create.html', methods=['GET'])
def create_html():
    return app.send_static_file('create.html')


@app.route('/create', methods=['POST'])
def create_note():
    text = request.form.get("text")

    key = crypt.generate_key()

    note_id = db.Note.create(
        text=crypt.encrypt_text(
            text,
            key
        )
    ).id

    return render_template(
        'code.html',
        code=crypt.encrypt_key(
            note_id,
            key
        )
    )


@app.route("/find", methods=['POST'])
def find():
    super_key = request.form.get("key")
    if super_key is None or super_key.strip() == "" or not super_key.isascii():
        return redirect("/")

    note_id, key = crypt.decrypt_key(super_key)

    if note_id is None:
        return render_template(
            "error.html",
            error="Invalid key"
        )

    encrypted_text = db.Note.get_text_by_id(note_id)

    if encrypted_text is None:
        return render_template(
            "error.html",
            error="Note not found"
        )

    else:
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

    Example correct request:
    {"text": "Hello there!"}

    Example correct answer:
    {"key": "gAAAAABhNQGGRwrwHkwydWFZfnt0N4gq"}

    Error answers:

    code - 400
    reason - json data is not valid

    """
    json_data = request.get_json(
        force=True,
        silent=True
    )
    if json_data is None or json_data.get("text") is None:
        return {
                   "error": "json data is not valid"
               }, 400

    key = crypt.generate_key()

    note_id = db.Note.create(
        text=crypt.encrypt_text(
            json_data.get("text"),
            key
        )
    ).id

    return {
        "key": crypt.encrypt_key(
            note_id,
            key
        )
    }


@app.route('/api/get', methods=["POST"])
def get():
    """
    This function checks if json_data is valid, then decrypt user access code and get id of Note.
    After that it decrypts text from note and sends back to user.

    Example correct request:
    {"key": "gAAAAABhNQGGRwrwHkwydWFZfnt0N4gq"}

    Example correct answer:
    {"text": "Hello there!"}

    Error answers:

    code - 400
    reason - json data is not valid

    code - 400
    reason - invalid key

    code - 404
    reason - note not found

    """
    json_data = request.get_json(
        force=True,
        silent=True
    )
    if json_data is None or json_data.get("key") is None or \
            json_data.get("key").strip() == "" or not json_data.get("key").isascii():
        return {
                   "error": "json data is not valid"
               }, 400

    note_id, key = crypt.decrypt_key(
        json_data.get("key")
    )

    if note_id is None:
        return {
                   "error": "invalid key",
               }, 400

    encrypted_text = db.Note.get_text_by_id(note_id)

    if encrypted_text is None:
        return {
                   "error": "note not found"
               }, 404

    return {
        "text": crypt.decrypt_text(
            encrypted_text,
            key
        )
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)