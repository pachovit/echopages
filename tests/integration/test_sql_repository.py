from echopages.domain import model
from echopages.infrastructure.database.sql import get_unit_of_work


def test_add_content_returns_id(dummy_db_uri: str) -> None:
    uow = get_unit_of_work(dummy_db_uri)

    content = model.Content(text="sample content unit 1")
    with uow:
        content_id = uow.content_repo.add(content)

    assert content_id is not None
