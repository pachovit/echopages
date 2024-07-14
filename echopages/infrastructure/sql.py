from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import echopages.config
from echopages.infrastructure.orm import metadata, start_mappers
from echopages.infrastructure.sql_repositories import SQLUnitOfWork

engine = None


def get_session_maker(db_uri: str) -> sessionmaker[Session]:
    global engine
    if engine is None:
        engine = create_engine(db_uri)
        metadata.create_all(engine)
        start_mappers()
    return sessionmaker(bind=engine)


def get_unit_of_work(db_uri: str = echopages.config.DB_URI) -> SQLUnitOfWork:
    return SQLUnitOfWork(get_session_maker(db_uri))
