import os
from typing import Generator

import pytest

TEST_DB_URI = "sqlite:///test.db"


@pytest.fixture(scope="session")
def dummy_db_uri() -> Generator[str, None, None]:
    yield TEST_DB_URI

    test_db_file = TEST_DB_URI.split("/")[-1]
    if os.path.exists(test_db_file):
        os.remove(test_db_file)
