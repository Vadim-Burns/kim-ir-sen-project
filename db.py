"""
This file manages database requests and connections
"""

from peewee import Model, TextField
from playhouse.db_url import connect

import config

db = connect(config.database_url)


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
        :param id: Id of the note
        :return: str text of the note
        """
        note = Note.get_by_id(id)

        text = note.text
        note.delete_instance()

        return text


Note.create_table()
