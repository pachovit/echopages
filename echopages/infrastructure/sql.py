from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from echopages.domain import model
from echopages.domain.repositories import ContentRepository
from echopages.infrastructure.orm import metadata, start_mappers

engine = None


def get_session_maker(db_uri):
    global engine
    if engine is None:
        engine = create_engine(db_uri)
        metadata.create_all(engine)
        start_mappers()
    return sessionmaker(bind=engine)


class SQLContentRepository(ContentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, content_id: int) -> Optional[model.Content]:
        return (
            self.db_session.query(model.Content)
            .filter(model.Content.id == content_id)  # type: ignore
            .first()
        )

    def get_all(self) -> List[model.Content]:
        return self.db_session.query(model.Content).all()

    def add(self, content: model.Content) -> int:
        self.db_session.add(content)
        self.db_session.commit()
        assert content.id is not None
        return content.id
