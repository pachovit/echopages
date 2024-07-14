from typing import Generator, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import echopages.config
from echopages.domain import model
from echopages.domain.repositories import (
    ContentRepository,
    DigestRepository,
    UnitOfWork,
)
from echopages.infrastructure.orm import metadata, start_mappers

engine = None


def get_session_maker(db_uri: str) -> sessionmaker[Session]:
    global engine
    if engine is None:
        engine = create_engine(db_uri)
        metadata.create_all(engine)
        start_mappers()
    return sessionmaker(bind=engine)


class SQLContentRepository(ContentRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_by_id(self, content_id: int) -> Optional[model.Content]:
        result = (
            self.db_session.query(model.Content)
            .filter(model.Content.id == content_id)  # type: ignore
            .first()
        )
        return result

    def get_all(self) -> List[model.Content]:
        return self.db_session.query(model.Content).all()

    def add(self, content: model.Content) -> int:
        self.db_session.add(content)
        self.db_session.flush()  # ID is assigned here
        assert content.id is not None
        return content.id


class SQLDigestRepository(DigestRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_by_id(self, digest_id: int) -> Optional[model.Digest]:
        return (
            self.db_session.query(model.Digest)
            .filter(model.Digest.id == digest_id)  # type: ignore
            .first()
        )

    def get_all(self) -> List[model.Digest]:
        return self.db_session.query(model.Digest).all()

    def add(self, digest: model.Digest) -> int:
        self.db_session.add(digest)
        self.db_session.flush()  # ID is assigned here
        assert digest.id is not None
        return digest.id


def get_content_repo(db_uri: str) -> SQLContentRepository:
    session_maker = get_session_maker(db_uri)
    db_session = session_maker()
    return SQLContentRepository(db_session)


def get_managed_content_repo(
    db_uri: str = echopages.config.DB_URI,
) -> Generator[SQLContentRepository, None, None]:
    content_repo = get_content_repo(db_uri)
    yield content_repo
    content_repo.db_session.close()


def get_digest_repo(db_uri: str) -> SQLDigestRepository:
    session_maker = get_session_maker(db_uri)
    db_session = session_maker()
    return SQLDigestRepository(db_session)


def get_managed_digest_repo(
    db_uri: str = echopages.config.DB_URI,
) -> Generator[SQLDigestRepository, None, None]:
    digest_repo = get_digest_repo(db_uri)
    yield digest_repo
    digest_repo.db_session.close()


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.content_repo = SQLContentRepository(self.session)
        self.digest_repo = SQLDigestRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


def get_unit_of_work(db_uri: str = echopages.config.DB_URI):
    return SqlAlchemyUnitOfWork(get_session_maker(db_uri))
