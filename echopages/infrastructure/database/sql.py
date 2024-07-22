from __future__ import annotations

from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    scoped_session,
    sessionmaker,
)

import echopages.config
from echopages.domain import model
from echopages.domain.repositories import (
    ContentRepository,
    DigestRepository,
    UnitOfWork,
)
from echopages.infrastructure.database.orm import metadata, start_mappers

engine = None


def get_session_factory(db_uri: str) -> scoped_session[Session]:
    global engine
    if engine is None:
        engine = create_engine(db_uri)
        metadata.create_all(engine)
        start_mappers()
    return scoped_session(sessionmaker(bind=engine))


def get_unit_of_work(db_uri: Optional[str] = None) -> SQLUnitOfWork:
    if db_uri is None:
        db_uri = echopages.config.DB_URI
    return SQLUnitOfWork(get_session_factory(db_uri))


class SQLContentRepository(ContentRepository):
    def __init__(self, db_session: Optional[Session] = None):
        self.db_session = db_session

    def get_by_id(self, content_id: int) -> Optional[model.Content]:
        assert self.db_session is not None
        result = (
            self.db_session.query(model.Content)
            .filter(model.Content.id == content_id)  # type: ignore
            .first()
        )
        return result

    def get_all(self) -> List[model.Content]:
        assert self.db_session is not None
        result = self.db_session.query(model.Content).all()
        return result

    def add(self, content: model.Content) -> int:
        assert self.db_session is not None
        self.db_session.add(content)
        self.db_session.flush()  # ID is assigned here
        self.db_session.expunge(content)
        assert content.id is not None
        return content.id


class SQLDigestRepository(DigestRepository):
    def __init__(self, db_session: Optional[Session] = None):
        self.db_session = db_session

    def get_by_id(self, digest_id: int) -> Optional[model.Digest]:
        assert self.db_session is not None
        result = (
            self.db_session.query(model.Digest)
            .filter(model.Digest.id == digest_id)  # type: ignore
            .first()
        )
        assert result is not None
        return result

    def get_all(self) -> List[model.Digest]:
        assert self.db_session is not None
        result = self.db_session.query(model.Digest).all()
        return result

    def add(self, digest: model.Digest) -> int:
        assert self.db_session is not None
        self.db_session.add(digest)
        self.db_session.flush()  # ID is assigned here
        assert digest.id is not None
        return digest.id

    def update(self, digest: model.Digest) -> None:
        assert self.db_session is not None
        self.db_session.add(digest)


class SQLUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        super().__init__()
        self.session_factory = session_factory

    def __enter__(self) -> UnitOfWork:
        if not self.entered:
            self.session: Session = self.session_factory()
            self.content_repo = SQLContentRepository(self.session)
            self.digest_repo = SQLDigestRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args) -> None:  # type: ignore
        super().__exit__(*args)
        self.session.close()

    def _commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
