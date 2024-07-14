from echopages.infrastructure import samplers, sql
from echopages.infrastructure.fakes import (
    FakeContentRepository,
    FakeDigestDeliverySystem,
    FakeDigestRepository,
)
from echopages.infrastructure.sql import SessionLocal, SQLContentRepository


def get_sql_content_repo():
    db_session = SessionLocal()
    return SQLContentRepository(db_session)


content_repo = None


def get_fake_content_repo():
    global content_repo
    if content_repo is None:
        content_repo = FakeContentRepository([])
    return content_repo


def get_content_repo():
    return get_sql_content_repo()


def bootstrap():
    content_repo = sql.SQLContentRepository(sql.SessionLocal())
    digest_repo = FakeDigestRepository([])
    delivery_system = FakeDigestDeliverySystem()
    content_sampler = samplers.SimpleContentSampler()
