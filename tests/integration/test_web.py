from fastapi.testclient import TestClient
from httpx import Response

from echopages.api import endpoints

client = TestClient(endpoints.app)


def _add_content(url: str, content: str) -> Response:
    r = client.post(f"{url}/add_content", json={"text": content})
    assert r.status_code == 201, f"Failed with status {r.status_code}: {r.json()}"
    return r


def test_add_content() -> None:
    content = "sample content unit 1"
    url = "http://127.0.0.1:8000"

    r = _add_content(url, content)
    assert r.status_code == 201

    content_id = r.json()["content_id"]

    r = client.get(f"{url}/contents/{content_id}")
    assert r.status_code == 200
    assert r.json()["text"] == content


def test_trigger_digest() -> None:
    url = "http://127.0.0.1:8000"
    _add_content(url, "sample content 123")

    r = client.post(f"{url}/trigger_digest", json={"n_units": 2})

    assert r.status_code == 200
    assert "sample content 123" in r.json()["digest_str"]


def test_configure_schedule() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/configure_schedule", json={"time_of_day": "08:00"})

    assert r.status_code == 200


def test_configure_schedule_fails_validation() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/configure_schedule", json={"time_of_day": "08:00:01"})

    assert r.status_code == 422
