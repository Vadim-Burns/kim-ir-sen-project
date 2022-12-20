from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_CONNECT_URL
from entities import Base


def init_db_connection() -> sessionmaker:
    """MUST BE CALLED ONLY ONCE"""
    _engine = create_engine(
        DATABASE_CONNECT_URL
    )

    # Generate all tables if doesn't exists
    Base.metadata.create_all(_engine)

    return sessionmaker(autocommit=False, autoflush=False, bind=_engine)
