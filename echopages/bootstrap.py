import echopages.config
from echopages.infrastructure.sql import SQLContentRepository, get_session_maker


def get_content_repo(db_uri=echopages.config.DB_URI):
    session_maker = get_session_maker(db_uri)
    db_session = session_maker()
    yield SQLContentRepository(db_session)
    db_session.close()
