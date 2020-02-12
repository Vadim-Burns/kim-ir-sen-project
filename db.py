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
