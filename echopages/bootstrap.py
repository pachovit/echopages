from typing import Generator

import echopages.config
from echopages.infrastructure.sql import SQLContentRepository, get_session_maker


def get_content_repo(db_uri: str) -> SQLContentRepository:
    session_maker = get_session_maker(db_uri)
    db_session = session_maker()
    return SQLContentRepository(db_session)


def get_managed_content_repo(
    db_uri: str = echopages.config.DB_URI,
) -> Generator[SQLContentRepository, None, None]:
    content_repo = get_content_repo(db_uri)
    yield content_repo
    content_repo.db_session.close()
