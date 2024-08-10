from typing import Dict, List

from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenario, then, when

from echopages.setup_app import create_app

app = create_app(frontend=False)
client = TestClient(app)


@scenario("get_all_content.feature", "Successfully get all content")
def test_add_content() -> None:
    pass


def add_content(source: str, author: str, location: str, text: str) -> Dict[str, str]:
    content_metadata = {
        "source": source,
        "author": author,
        "location": location,
        "text": text,
    }
    response = client.post("/api/add_content", json=content_metadata)
    assert response.status_code == 201
    return content_metadata


@given(
    parsers.parse("10 content units previously added"),
    target_fixture="existing_content",
)
def given_content() -> List[Dict[str, str]]:
    existing_content = []
    for i in range(10):
        source = f"Book Name {i}"
        author = f"One Author {i}"
        location = f"Chapter {i}"
        text = f"summary {i}"
        content_dict = add_content(source, author, location, text)
        existing_content.append(content_dict)

    return existing_content


@when("I request all content", target_fixture="gotten_content")
def get_all_content() -> List[Dict[str, str]]:
    response = client.get("/api/contents")
    assert response.status_code == 200
    gotten_content = response.json()
    assert isinstance(gotten_content, list)
    return gotten_content


@then("I should get all 10 elements with IDs")
def all_10_elements(
    gotten_content: List[Dict[str, str]], existing_content: List[Dict[str, str]]
) -> None:
    assert len(gotten_content) == len(existing_content)
    for content in gotten_content:
        content_id = content.pop("id")
        assert content_id is not None
        assert content in existing_content
