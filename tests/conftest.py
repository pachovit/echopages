import pytest

from echopages.infrastructure.sql import get_session_maker


@pytest.fixture(scope="session")
def db_session():
    session_maker = get_session_maker()
    session = session_maker()
    yield session
    session.close()
