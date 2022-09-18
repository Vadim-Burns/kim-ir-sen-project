"""
This file contains flask server for processing requests
"""

import inject
from flask import Flask

import config
from endpoints import AbstractEndpoint
from services import AbstractKimService


# app = Flask(__name__, static_folder=config.FLASK_STATIC_FOLDER)
#
#
#
#
#
# @app.errorhandler(404)
# def error_404(error):
#     return redirect("/")
#
#
# @app.route('/create.html', methods=['GET'])
# def create_html():
#     return app.send_static_file('create.html')
#
#
# @app.route('/create', methods=['POST'])
# def create_note():
#     text = request.form.get("text")
#     return render_template(
#         'code.html',
#         code=kim_service.save_note(text)
#     )
#
#
# @app.route("/find", methods=['POST'])
# def find():
#     super_key = request.form.get("key")
#     if super_key is None or super_key.strip() == "" or not super_key.isascii():
#         return redirect("/")
#
#     note = kim_service.get_note(super_key)
#     if note is None:
#         return render_template(
#             "error.html",
#             error="Invalid key"
#         )
#
#     return render_template(
#         "note.html",
#         text=kim_service.get_note(super_key)
#     )
#
#
# @app.route('/api/add', methods=["POST"])
# def add():
#     """
#     This function checks if json_data is valid, then generate random key and save
#     encrypt_serviceed text to database. Then generates access code for user note.id + "=" + key for text.
#
#     Example correct request:
#     {"text": "Hello there!"}
#
#     Example correct answer:
#     {"key": "gAAAAABhNQGGRwrwHkwydWFZfnt0N4gq"}
#
#     Error answers:
#
#     code - 400
#     reason - json data is not valid
#
#     """
#     json_data = request.get_json(
#         force=True,
#         silent=True
#     )
#     if json_data is None or json_data.get("text") is None:
#         return {
#                    "error": "json data is not valid"
#                }, 400
#
#     return {
#         "key": kim_service.save_note(json_data.get("text"))
#     }
#
#
# @app.route('/api/get', methods=["POST"])
# def get():
#     """
#     This function checks if json_data is valid, then decrypt_service user access code and get id of Note.
#     After that it decrypt_services text from note and sends back to user.
#
#     Example correct request:
#     {"key": "gAAAAABhNQGGRwrwHkwydWFZfnt0N4gq"}
#
#     Example correct answer:
#     {"text": "Hello there!"}
#
#     Error answers:
#
#     code - 400
#     reason - json data is not valid
#
#     code - 403
#     reason - Invalid key
#
#     """
#     json_data = request.get_json(
#         force=True,
#         silent=True
#     )
#     if json_data is None or json_data.get("key") is None or \
#             json_data.get("key").strip() == "" or not json_data.get("key").isascii():
#         return {
#                    "error": "json data is not valid"
#                }, 400
#
#     note = kim_service.get_note(json_data.get("key"))
#     if note is None:
#         return {
#                    "error": "Invalid key"
#                }, 403
#
#     return {
#         "text": note
#     }


class WebEndpoint(AbstractEndpoint):

    @inject.autoparams('kim_service')
    def __init__(self, host: str, port: int, kim_service: AbstractKimService):
        self._host = host
        self._port = port

        self._kim_service = kim_service
        self._app = Flask("kim", static_folder=config.FLASK_STATIC_FOLDER)

        self._init_mapping()

    def _init_mapping(self):
        self._app.add_url_rule('/', None, self.index, methods=['GET'])

    def run(self):
        self._app.run(host=self._host, port=self._port)

    def get_name(self) -> str:
        return "Web(Flask)"

    def index(self):
        return self._app.send_static_file('index.html')
