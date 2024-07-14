from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session, sessionmaker

from echopages.domain import model
from echopages.domain.repositories import (
    ContentRepository,
    DigestRepository,
    UnitOfWork,
)


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


class SQLUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def __enter__(self) -> UnitOfWork:
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
