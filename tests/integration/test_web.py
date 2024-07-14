from fastapi.testclient import TestClient

from echopages.infrastructure import web

client = TestClient(web.app)


def test_add_content() -> None:
    content = "sample content unit 1"
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/add_content", json={"text": content})
    assert r.status_code == 201

    content_id = r.json()["content_id"]

    r = client.get(f"{url}/contents/{content_id}")
    assert r.status_code == 200
    assert r.json()["text"] == content


def test_trigger_digest() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/trigger_digest", json={"n_units": 2})

    assert r.status_code == 200
    assert len(r.json()["digest"]) == 2


def test_configure_schedule() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/configure_schedule", json={"time_of_day": "08:00"})

    assert r.status_code == 200


def test_configure_schedule_fails_validation() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/configure_schedule", json={"time_of_day": "08:00:01"})

    assert r.status_code == 422
