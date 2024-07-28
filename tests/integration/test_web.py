from typing import Dict

from fastapi.testclient import TestClient
from httpx import Response

from echopages.api import endpoints

client = TestClient(endpoints.app)


def _add_content(url: str, content_data: Dict[str, str]) -> Response:
    r = client.post(f"{url}/add_content", json=content_data)
    assert r.status_code == 201, f"Failed with status {r.status_code}: {r.json()}"
    return r


def test_trigger_digest() -> None:
    url = "http://127.0.0.1:8000"
    content_data = {
        "source": "sample source",
        "author": "sample author",
        "location": "sample location",
        "text": "sample content 123",
    }
    _add_content(url, content_data)

    r = client.post(f"{url}/trigger_digest", json={"n_units": 2})

    assert r.status_code == 200
    assert "sample source" in r.json()["digest_content_str"]
    assert "sample author" in r.json()["digest_content_str"]
    assert "sample location" in r.json()["digest_content_str"]
    assert "sample content 123" in r.json()["digest_content_str"]
    assert "sample source" in r.json()["digest_title"]


def test_configure_schedule() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/configure_schedule", json={"time_of_day": "08:00"})

    assert r.status_code == 200


def test_configure_schedule_fails_validation() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/configure_schedule", json={"time_of_day": "08:00:01"})

    assert r.status_code == 422
