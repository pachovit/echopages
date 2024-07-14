from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import registry, relationship

from echopages.domain import model

metadata = MetaData()

contents = Table(
    "contents",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("text", String),
)

digests = Table(
    "digests",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sent", Boolean, default=False),
)
digest_content_association = Table(
    "digest_content_association",
    metadata,
    Column("digest_id", Integer, ForeignKey("digests.id")),
    Column("content_id", Integer, ForeignKey("contents.id")),
)


def start_mappers() -> None:
    mapper_registry = registry()
    mapper_registry.map_imperatively(model.Content, contents)
    mapper_registry.map_imperatively(
        model.Digest,
        digests,
        properties={
            "contents": relationship(
                model.Content, secondary=digest_content_association
            )
        },
    )
