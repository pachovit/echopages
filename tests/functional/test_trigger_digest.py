from fastapi.testclient import TestClient
from httpx import Response
from pytest_bdd import given, scenario, then, when

from echopages.main import app

client = TestClient(app)
host_url = "http://127.0.0.1:8000/api"


@scenario("trigger_digest.feature", "Successfully trigger a digest")
def test_trigger_digest() -> None:
    pass


@given("some already added contents")
def add_contents() -> None:
    content_data = {
        "source": "sample source",
        "author": "sample author",
        "location": "sample location",
        "text": "sample content 123",
    }
    r = client.post(f"{host_url}/add_content", json=content_data)
    assert r.status_code == 201, f"Failed with status {r.status_code}: {r.json()}"


@when("I trigger a digest", target_fixture="trigger_digest_response")
def trigger_digest() -> Response:
    r = client.post(f"{host_url}/trigger_digest", json={"n_units": 2})
    return r


@then("the digest should be delivered with some content")
def digest_is_delivered(trigger_digest_response: Response) -> None:
    assert trigger_digest_response.status_code == 200
    assert "sample source" in trigger_digest_response.json()["digest_content_str"]
    assert "sample author" in trigger_digest_response.json()["digest_content_str"]
    assert "sample location" in trigger_digest_response.json()["digest_content_str"]
    assert "sample content 123" in trigger_digest_response.json()["digest_content_str"]
    assert "sample source" in trigger_digest_response.json()["digest_title"]
