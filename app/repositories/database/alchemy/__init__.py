from functools import wraps
from typing import List
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.orm.session import Session

from entities import BaseEntity, NoteEntity
from repositories.database import AbstractRepo, AbstractNoteRepo
from repositories.database.alchemy.connect import init_db_connection

SessionMaker = init_db_connection()


def session_maker(func):
    @wraps(func)
    def wrapper(*args, **params):
        with SessionMaker() as session:
            return func(*args, **params, session=session)

    return wrapper


class AlchemyRepo(AbstractRepo):
    entity = None

    @session_maker
    def update(
            self,
            session: Session,
            pk_key: UUID,
            **params
    ) -> None:
        session.query(self.entity).filter_by(id=pk_key).update(params, synchronize_session="fetch")
        session.commit()

    @session_maker
    def save_instances(self, session: Session, instances: List[BaseEntity]) -> list[BaseEntity]:
        session.add_all(instances=instances)
        session.commit()

        for inst in instances:
            session.refresh(inst)

        return instances

    @session_maker
    def list(self, session: Session, **params):
        q = session.query(self.entity).filter_by(**params).order_by(self.entity.created_at.desc())

        return q

    @session_maker
    def get(self, session: Session, **params) -> entity:
        instance = session.query(self.entity).filter_by(**params).order_by(self.entity.created_at.desc()).first()
        if instance:
            return instance

        return None

    @session_maker
    def exists(self, session: Session, **params) -> bool:
        return session.query(session.query(self.entity).filter_by(**params).exists()).scalar()

    @session_maker
    def count(self, session: Session, **params) -> int:
        return session.query(self.entity).filter_by(**params).count()

    @session_maker
    def delete(self, session: Session, id: int) -> None:
        sq = delete(self.entity).where(self.entity.id == id)
        session.execute(sq)
        session.commit()


class NoteRepo(AbstractNoteRepo, AlchemyRepo):
    entity = NoteEntity
