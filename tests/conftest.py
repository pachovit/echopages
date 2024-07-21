import os
from typing import Generator

import pytest

TEST_DB_URI = "sqlite:///test.db"


@pytest.fixture(scope="session", autouse=True)
def dummy_db_uri() -> Generator[str, None, None]:
    os.environ["DB_URI"] = TEST_DB_URI
    yield TEST_DB_URI

    test_db_file = TEST_DB_URI.split("/")[-1]
    if os.path.exists(test_db_file):
        os.remove(test_db_file)


@pytest.fixture(scope="session", autouse=True)
def fake_delivery_system() -> Generator[str, None, None]:
    os.environ["DELIVERY_SYSTEM"] = "FakeDigestDeliverySystem"
    yield "FakeDigestDeliverySystem"

    os.environ.pop("DELIVERY_SYSTEM")
