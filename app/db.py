"""
This file manages database requests and connections
"""

from peewee import Model, TextField
from playhouse.db_url import connect

import config

db = connect(config.DATABASE_CONNECT_URL)


class BadeModel(Model):
    class Meta:
        database = db
        only_save_dirty = True


class Note(BadeModel):
    text = TextField()

    @staticmethod
    def get_text_by_id(id: int) -> str:
        """
        Returns text of the note by note's id
        and delete note after that

        If there is no note in database 'None' will be returned

        :param id: Id of the note
        :return: str text of the note
        """
        note = Note.get_or_none(Note.id == id)

        if note is None:
            return None
        else:
            text = note.text
            note.delete_instance()

            return text


Note.create_table()
