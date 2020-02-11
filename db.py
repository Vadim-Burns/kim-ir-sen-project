from peewee import Model, TextField
import os
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL'))


class Note(Model):
    text = TextField()

    class Meta:
        database = db

    @staticmethod
    def get_text_by_id(id):
        try:
            note = Note.get_by_id(id)
            text = note.text
            note.delete_instance()
            return text
        except:
            return None


Note.create_table()

if __name__ == '__main__':
    import requests

    key = requests.post("http://127.0.0.1:5000/api/add", json={"text": "hfdhahfdas"}).json().get("key")
    print(key)
    text = requests.post("http://127.0.0.1:5000/api/get", json={"key": key}).json().get("text")
    print(text)
