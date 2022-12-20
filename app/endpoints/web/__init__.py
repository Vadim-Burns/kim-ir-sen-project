"""
This file contains flask server for processing requests
"""

import inject
from flask import Flask, redirect, request, render_template

import config
from endpoints import AbstractEndpoint
from services import AbstractKimService


class WebEndpoint(AbstractEndpoint):

    @inject.autoparams('kim_service')
    def __init__(self, host: str, port: int, kim_service: AbstractKimService):
        self._host = host
        self._port = port

        self._kim_service = kim_service
        self._app = Flask("kim", static_folder=config.FLASK_STATIC_FOLDER, template_folder=config.FLASK_TEMPLATE_FOLDER)

        self._init_mapping()

    def _init_mapping(self):
        """
        Init flask url mapping
        """
        # Web
        self._app.add_url_rule('/', None, self.index, methods=['GET'])
        self._app.register_error_handler(404, self.error_404)
        self._app.add_url_rule('/create.html', None, self.create_html, methods=['GET'])
        self._app.add_url_rule('/create', None, self.create_note, methods=['POST'])
        self._app.add_url_rule('/find', None, self.find, methods=['POST'])

        # Api
        self._app.add_url_rule('/api/add', None, self.add, methods=['POST'])
        self._app.add_url_rule('/api/get', None, self.get, methods=['POST'])

    def run(self):
        self._app.run(host=self._host, port=self._port)

    def get_name(self) -> str:
        return "Web(Flask)"

    def index(self):
        return self._app.send_static_file('index.html')

    def error_404(self, error):
        return redirect("/")

    def create_html(self):
        return self._app.send_static_file('create.html')

    def create_note(self):
        text = request.form.get("text")
        return render_template(
            'code.html',
            code=self._kim_service.save_note(text)
        )

    def find(self):
        super_key = request.form.get("key")
        if super_key is None or super_key.strip() == "" or not super_key.isascii():
            return redirect("/")

        note = self._kim_service.get_note(super_key)
        if note is None:
            return render_template(
                "error.html",
                error="Invalid key"
            )

        return render_template(
            "note.html",
            text=note
        )

    def add(self):
        """
        This function checks if json_data is valid, then generate random key and save
        encrypt_serviceed text to database. Then generates access code for user note.id + "=" + key for text.

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

        return {
            "key": self._kim_service.save_note(json_data.get("text"))
        }

    def get(self):
        """
        This function checks if json_data is valid, then decrypt_service user access code and get id of Note.
        After that it decrypt_services text from note and sends back to user.

        Example correct request:
        {"key": "gAAAAABhNQGGRwrwHkwydWFZfnt-1N4gq"}

        Example correct answer:
        {"text": "Hello there!"}

        Error answers:

        code - 400
        reason - json data is not valid

        code - 403
        reason - Invalid key

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

        note = self._kim_service.get_note(json_data.get("key"))
        if note is None:
            return {
                       "error": "Invalid key"
                   }, 403

        return {
            "text": note
        }
