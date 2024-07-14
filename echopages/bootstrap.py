from echopages.infrastructure.sql import SQLContentRepository, get_session_maker


def get_content_repo():
    session_maker = get_session_maker()
    db_session = session_maker()
    yield SQLContentRepository(db_session)
    db_session.close()
