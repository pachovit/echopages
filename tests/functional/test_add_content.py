from unittest.mock import Mock

from fastapi.testclient import TestClient
from pytest_bdd import given, scenario, then, when

from echopages.api.endpoints import app  # Import your FastAPI app

client = TestClient(app)


@scenario(
    "add_content.feature", "Successfully add content", features_base_dir="features"
)
def test_add_content() -> None:
    pass


@given("the user is on the add content page")
def step_given_user_on_add_content_page(context: Mock) -> None:
    pass


@when("the user enters valid content text")
def step_when_user_enters_valid_content_text(context: Mock) -> None:
    context.sent_text = "This is a valid content text"


@when("clicks the submit button")
def step_when_user_clicks_submit_button(context: Mock) -> None:
    context.response = client.post(
        "/add_content", json={"text": context.sent_text}
    )  # Adjust the endpoint as necessary


@then("the content should be saved")
def step_then_content_should_be_saved(context: Mock) -> None:
    assert context.response.status_code == 201
    context.content_id = context.response.json()["content_id"]
    assert context.content_id is not None


@then("content should be retrievable")
def step_and_content_should_be_retrievable(context: Mock) -> None:
    context.response = client.get(f"/contents/{context.content_id}")
    assert context.response.status_code == 200
    context.gotten_text = context.response.json()["text"]
    assert context.gotten_text == context.sent_text
