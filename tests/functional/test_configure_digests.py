from fastapi.testclient import TestClient
from httpx import Response
from pytest_bdd import given, scenario, then, when
from typing import Dict, Any
from echopages.api import endpoints

client = TestClient(endpoints.app)
host_url = "http://127.0.0.1:8000"


@scenario("configure_digests.feature", "Successfully reconfigure a digest")
def test_reconfigure_digest() -> None:
    pass


@given("a previous configuration", target_fixture="config")
def get_config() -> None:
    r = client.get(f"{host_url}/get_config")
    assert r.status_code == 200, f"Failed with status {r.status_code}: {r.json()}"
    return r.json()


@when("I send new configuration parameters", target_fixture="new_config_params")
def update_config(config) -> Response:
    new_number_of_units_per_digest = config["number_of_units_per_digest"] + 1
    new_daily_time_of_digests = "12:34"
    assert config["daily_time_of_digest"] != new_daily_time_of_digests
    config = {"number_of_units_per_digest": new_number_of_units_per_digest,"daily_time_of_digest": new_daily_time_of_digests}
    
    r = client.post(f"{host_url}/set_config", json=config)
    assert r.status_code == 201, f"Failed with status {r.status_code}: {r.json()}"
    return config


@then("the configuration is updated")
def config_is_updated(new_config_params: Dict[str, Any]) -> None:    
    new_number_of_units_per_digest = new_config_params["number_of_units_per_digest"]
    new_daily_time_of_digests = new_config_params["daily_time_of_digest"]
    r = client.get(f"{host_url}/get_config")
    assert r.status_code == 200, f"Failed with status {r.status_code}: {r.json()}"
    new_config = r.json()

    assert new_config["number_of_units_per_digest"] == new_number_of_units_per_digest
    assert new_config["daily_time_of_digest"] == new_daily_time_of_digests