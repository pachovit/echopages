from echopages.infrastructure.sql import SessionLocal, SQLContentRepository


def get_sql_content_repo():
    db_session = SessionLocal()
    return SQLContentRepository(db_session)


def get_content_repo():
    return get_sql_content_repo()
