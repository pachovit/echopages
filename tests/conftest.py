import os
from typing import Generator
from unittest.mock import patch

import pytest

TEST_DB_URI = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def dummy_db_uri() -> Generator[str, None, None]:
    with patch("echopages.config.DB_URI", TEST_DB_URI):
        yield


@pytest.fixture(scope="session", autouse=True)
def fake_delivery_system() -> Generator[str, None, None]:
    os.environ["DELIVERY_SYSTEM"] = "FakeDigestDeliverySystem"
    yield "FakeDigestDeliverySystem"

    os.environ.pop("DELIVERY_SYSTEM")
