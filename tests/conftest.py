import os
import shutil
from typing import Generator
from unittest.mock import patch

import pytest

TEST_DB_URI = "./test.db"


@pytest.fixture(scope="function", autouse=True)
def dummy_db_uri() -> Generator[None, None, None]:
    with patch("echopages.config.DB_URI", TEST_DB_URI):
        yield

    if os.path.exists(TEST_DB_URI):
        shutil.rmtree(TEST_DB_URI)


@pytest.fixture(scope="session", autouse=True)
def fake_delivery_system() -> Generator[None, None, None]:
    with patch("echopages.config.DELIVERY_SYSTEM", "FakeDigestDeliverySystem"):
        yield
