from echopages.domain import model
from echopages.infrastructure.database.sql import get_content_repo


def test_add_content_returns_id(dummy_db_uri: str) -> None:
    content_repo = get_content_repo(dummy_db_uri)
    content = model.Content(text="sample content unit 1")

    content_id = content_repo.add(content)

    assert content_id is not None
