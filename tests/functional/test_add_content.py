from typing import Dict

from fastapi.testclient import TestClient
from httpx import Response
from pytest_bdd import given, parsers, scenario, then, when

from echopages.setup_app import create_app

app = create_app(frontend=False)
client = TestClient(app)


@scenario("add_content.feature", "Successfully add content")
def test_add_content() -> None:
    pass


@scenario("add_content.feature", "Not adding content when not specifying text")
def test_add_content_missing_text() -> None:
    pass


@given(
    parsers.parse(
        (
            "a content with source {source}, author {author}, "
            "location {location}, and text {text}"
        )
    ),
    target_fixture="content_metadata",
)
def given_content(source: str, author: str, location: str, text: str) -> Dict[str, str]:
    content_metadata = dict()
    if source != "<none>":
        content_metadata["source"] = source
    if author != "<none>":
        content_metadata["author"] = author
    if location != "<none>":
        content_metadata["location"] = location
    if text != "<none>":
        content_metadata["text"] = text

    return content_metadata


@when("I add the content", target_fixture="content_id")
def add_content(content_metadata: Dict[str, str]) -> int:
    response = client.post("/api/add_content", json=content_metadata)
    assert response.status_code == 201
    content_id = int(response.json()["content_id"])
    return content_id


@then("content should be retrievable")
def step_and_content_should_be_retrievable(
    content_metadata: Dict[str, str], content_id: int
) -> None:
    response = client.get(f"/api/contents/{content_id}")
    assert response.status_code == 200
    for key, value in content_metadata.items():
        assert response.json()[key] == value


@given(
    parsers.parse(
        (
            "a content without text, with source {source}, "
            "author {author}, location {location}"
        )
    ),
    target_fixture="content_metadata_without_text",
)
def given_content_missing_text(
    source: str, author: str, location: str
) -> Dict[str, str]:
    content_metadata = dict()
    if source != "<none>":
        content_metadata["source"] = source
    if author != "<none>":
        content_metadata["author"] = author
    if location != "<none>":
        content_metadata["location"] = location
    return content_metadata


@when("I add the content without text", target_fixture="failed_response")
def add_content_missing_text(content_metadata_without_text: Dict[str, str]) -> Response:
    response = client.post("/api/add_content", json=content_metadata_without_text)
    return response


@then("a 400 error should be raised")
def step_400_error_should_be_raised(failed_response: Response) -> None:
    assert failed_response.status_code == 400
    assert failed_response.json() == {"detail": "Text is required"}
