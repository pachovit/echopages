from fastapi.testclient import TestClient

from echopages.infrastructure import web

client = TestClient(web.app)


def test_add_content():
    content = "sample content unit 1"
    url = "http://127.0.0.1:8000"

    r = client.post(f"{url}/add_content", json={"text": content})
    assert r.status_code == 201

    content_id = r.json()["content_id"]

    r = client.get(f"{url}/contents/{content_id}")
    assert r.status_code == 200
    assert r.json()["text"] == content


# def test_configure_schedule():
#     url = "http://127.0.0.1:8000"

#     r = requests.post(f"{url}/configure_schedule", json={"time_of_day": "07:00"})

#     assert r.ok


# def test_generate_digest():
#     url = "http://127.0.0.1:8000"
#     number_of_units = 2
#     content = "sample content unit 1"
#     r = requests.post(f"{url}/add_content", json={"text": content})

#     r = requests.post(
#         f"{url}/generate_digest", json={"number_of_units": number_of_units}
#     )
#     assert r.ok

#     digest = r.json()["digest"]
#     assert len(digest) == number_of_units
#     assert all(digest == [content for _ in range(number_of_units)])
