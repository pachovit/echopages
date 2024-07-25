# features/steps/add_content_steps.py

from behave import given, then, when
from behave.runner import Context
from fastapi.testclient import TestClient

from echopages.api.endpoints import app  # Import your FastAPI app

client = TestClient(app)


@given("the user is on the add content page")  # type: ignore
def step_given_user_on_add_content_page(context: Context) -> None:
    pass


@when("the user enters valid content text")  # type: ignore
def step_when_user_enters_valid_content_text(context: Context) -> None:
    context.sent_text = "This is a valid content text"


@when("clicks the submit button")  # type: ignore
def step_when_user_clicks_submit_button(context: Context) -> None:
    context.response = client.post(
        "/add_content", json={"text": context.sent_text}
    )  # Adjust the endpoint as necessary


@then("the content should be saved")  # type: ignore
def step_then_content_should_be_saved(context: Context) -> None:
    assert context.response.status_code == 201
    context.content_id = context.response.json()["content_id"]
    assert context.content_id is not None


@then("content should be retrievable")  # type: ignore
def step_and_content_should_be_retrievable(context: Context) -> None:
    context.response = client.get(f"/contents/{context.content_id}")
    assert context.response.status_code == 200
    context.gotten_text = context.response.json()["text"]
    assert context.gotten_text == context.sent_text
