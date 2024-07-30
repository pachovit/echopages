from fastapi.testclient import TestClient

from echopages.api import endpoints

client = TestClient(endpoints.app)


def test_configure_schedule() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/configure_schedule", json={"time_of_day": "08:00"})

    assert r.status_code == 200


def test_configure_schedule_fails_validation() -> None:
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/configure_schedule", json={"time_of_day": "08:00:01"})

    assert r.status_code == 422
