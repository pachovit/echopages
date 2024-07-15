from __future__ import annotations

from functools import wraps
from typing import Any, Callable, List, Optional, TypeVar

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
)
from echopages.infrastructure.orm import metadata, start_mappers

engine = None


def get_session_factory(db_uri: str) -> scoped_session[Session]:
    global engine
    if engine is None:
        engine = create_engine(db_uri)
        metadata.create_all(engine)
        start_mappers()
    return scoped_session(sessionmaker(bind=engine))


def get_content_repo(db_uri: str = echopages.config.DB_URI) -> SQLContentRepository:
    return SQLContentRepository(get_session_factory(db_uri))


def get_digest_repo(db_uri: str = echopages.config.DB_URI) -> SQLDigestRepository:
    return SQLDigestRepository(get_session_factory(db_uri))


T = TypeVar("T")  # Generic return type


def handle_session(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self: "SQLAlchemyRepository", *args: Any, **kwargs: Any) -> T:
        self.db_session = self.session_factory()
        try:
            result: T = func(self, *args, **kwargs)
            self.db_session.commit()
            return result
        except Exception as e:
            self.db_session.rollback()
            raise e
        finally:
            self.db_session.close()  # Assuming each session should be closed after the operation
            self.db_session = None

    return wrapper


class SQLAlchemyRepository:
    def __init__(self, session_factory: scoped_session[Session]) -> None:
        self.session_factory = session_factory
        self.db_session: Optional[Session] = None


class SQLContentRepository(ContentRepository, SQLAlchemyRepository):
    @handle_session
    def get_by_id(self, content_id: int) -> Optional[model.Content]:
        result = (
            self.db_session.query(model.Content)
            .filter(model.Content.id == content_id)  # type: ignore
            .first()
        )
        self.db_session.expunge(result)

        return result

    @handle_session
    def get_all(self) -> List[model.Content]:
        result = self.db_session.query(model.Content).all()
        for element in result:
            self.db_session.expunge(element)
        return result

    @handle_session
    def add(self, content: model.Content) -> int:
        self.db_session.add(content)
        self.db_session.flush()  # ID is assigned here
        self.db_session.expunge(content)
        assert content.id is not None
        return content.id


class SQLDigestRepository(DigestRepository, SQLAlchemyRepository):
    @handle_session
    def get_by_id(self, digest_id: int) -> Optional[model.Digest]:
        result = (
            self.db_session.query(model.Digest)
            .filter(model.Digest.id == digest_id)  # type: ignore
            .first()
        )
        for el in result.contents:
            self.db_session.expunge(el)
        self.db_session.expunge(result)

        return result

    @handle_session
    def get_all(self) -> List[model.Digest]:
        result = self.db_session.query(model.Digest).all()
        for element in result:
            self.db_session.expunge(element)
        return result

    @handle_session
    def add(self, digest: model.Digest) -> int:
        self.db_session.add(digest)
        self.db_session.flush()  # ID is assigned here
        self.db_session.expunge(digest)
        assert digest.id is not None
        return digest.id

    @handle_session
    def update(self, digest: model.Digest) -> None:
        self.db_session.add(digest)
        self.db_session.expunge(digest)
