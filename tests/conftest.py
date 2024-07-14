import os
from typing import Generator

import pytest
from sqlalchemy.orm import Session

from echopages.infrastructure.sql import get_session_maker

TEST_DB_URI = "sqlite:///test.db"


@pytest.fixture(scope="session")
def db_session() -> Generator[Session, None, None]:
    session_maker = get_session_maker(TEST_DB_URI)
    session = session_maker()
    yield session
    session.close()
    test_db_file = TEST_DB_URI.split("/")[-1]
    if os.path.exists(test_db_file):
        os.remove(test_db_file)
