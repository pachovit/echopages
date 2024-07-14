from echopages.domain import model
from echopages.infrastructure.sql import SQLContentRepository


def test_add_content_returns_id(db_session):
    content_repo = SQLContentRepository(db_session)
    content = model.Content(text="sample content unit 1")

    content_id = content_repo.add(content)

    assert content_id == content.id
