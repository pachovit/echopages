from sqlalchemy.orm import Session

from echopages.domain import model
from echopages.infrastructure.sql_repositories import SQLContentRepository


def test_add_content_returns_id(db_session: Session) -> None:
    content_repo = SQLContentRepository(db_session)
    content = model.Content(text="sample content unit 1")

    content_id = content_repo.add(content)
    content_repo.db_session.commit()

    assert content_id == content.id
