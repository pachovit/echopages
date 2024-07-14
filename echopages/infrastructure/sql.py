from typing import List

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

    def get_by_id(self, content_unit_id: str) -> model.ContentUnit:
        return (
            self.db_session.query(model.ContentUnit)
            .filter(model.ContentUnit.id == content_unit_id)
            .first()
        )

    def get_all(self) -> List[model.ContentUnit]:
        return self.db_session.query(model.ContentUnit).all()

    def add(self, content_unit: model.ContentUnit) -> int:
        self.db_session.add(content_unit)
        self.db_session.commit()
        return content_unit.id
