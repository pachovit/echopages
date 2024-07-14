from echopages.domain import model
from echopages.infrastructure.sql import SQLContentRepository


def test_add_content_returns_id(db_session):
    content_repo = SQLContentRepository(db_session)
    content_unit = model.ContentUnit(text="sample content unit 1")

    content_unit_id = content_repo.add(content_unit)

    assert content_unit_id == content_unit.id
