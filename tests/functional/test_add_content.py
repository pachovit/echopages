from typing import Dict

from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenario, then, when

from echopages.api.endpoints import app

client = TestClient(app)


@scenario("add_content.feature", "Successfully add content")
def test_add_content() -> None:
    pass


@given(
    parsers.parse(
        "a content with source {source}, author {author}, location {location}, and text {text}"
    ),
    target_fixture="content_metadata",
)
def given_content(source: str, author: str, location: str, text: str) -> Dict[str, str]:
    content_metadata = {
        "source": source,
        "author": author,
        "location": location,
        "text": text,
    }
    return content_metadata


@when("I add the content", target_fixture="content_id")
def add_content(content_metadata: Dict[str, str]) -> int:
    response = client.post("/add_content", json=content_metadata)
    assert response.status_code == 201
    content_id = int(response.json()["content_id"])
    return content_id


@then("content should be retrievable")
def step_and_content_should_be_retrievable(
    content_metadata: Dict[str, str], content_id: int
) -> None:
    response = client.get(f"/contents/{content_id}")
    assert response.status_code == 200
    for key, value in content_metadata.items():
        assert response.json()[key] == value
