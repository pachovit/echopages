import os
import shutil
from typing import Generator
from unittest.mock import patch

import pytest

from echopages.config import get_config

TEST_DB_URI = "./test.db"
TEST_DIGESTS_DIR = "./test_digests"
TEST_DELIVERY_SYSTEM = "FileDigestDeliverySystem"


@pytest.fixture(scope="function", autouse=True)
def dummy_db_uri() -> Generator[None, None, None]:
    config = get_config()
    config.db_uri = TEST_DB_URI
    with patch("echopages.config.config", config):
        yield

    if os.path.exists(TEST_DB_URI):
        shutil.rmtree(TEST_DB_URI)


@pytest.fixture(scope="function", autouse=True)
def fake_delivery_system() -> Generator[None, None, None]:
    config = get_config()
    config.delivery_system = TEST_DELIVERY_SYSTEM
    config.file_delivery_system_directory = TEST_DIGESTS_DIR
    with patch("echopages.config.config", config):
        yield
    if os.path.exists(TEST_DIGESTS_DIR):
        shutil.rmtree(TEST_DIGESTS_DIR)
