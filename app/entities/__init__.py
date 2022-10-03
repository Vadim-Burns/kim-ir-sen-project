"""Object for database"""
import datetime

from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.sql import func

Base: DeclarativeMeta = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=func.now())

    def dict(self) -> dict:
        return self.__dict__


class NoteEntity(BaseEntity):
    __tablename__ = "notes"

    text = Column(Text)
