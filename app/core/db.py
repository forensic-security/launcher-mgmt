from typing import AsyncIterator

from sqlmodel import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from ..config import settings
from ..logger import log
from .model import Schema


engine = create_engine(settings.db_uri, pool_size=20)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def get_db() -> AsyncIterator[Session]:
    try:
        session = SessionLocal()
    except Exception as e:
        log.debug('%r --- %s', e, dir(e))
        raise

    try:
        yield session
        session.commit()
    finally:
        session.close()


def check_db(drop=False):
    from sqlalchemy_utils import database_exists, create_database, drop_database

    def get_users(users=[]):
        users.extend([
            {'username': 'dev@forensics.group', 'enabled': True, 'password': 'secret'},
            {'username': 'lisardo.prieto@datos101.com', 'enabled': True, 'password': 'forensics'},
        ])

        return users

    def add(session, item):
        try:
            session.add(item)
            session.commit()
        except Exception as e:
            session.rollback()
            log.error('%r', e)

    def populate():
        from app.models.user import User

        with SessionLocal() as session:
            for user in get_users():
                log.warning(add(session, User(**user)))

    if drop and database_exists(engine.url):
        log.warning('Deleting database: %r', engine.url)
        drop_database(engine.url)

    if not database_exists(engine.url):
        log.warning('Creating database: %r', engine.url)
        create_database(engine.url)
        Schema.metadata.schema = 'public'
        Schema.metadata.create_all(bind=engine)
        populate()
