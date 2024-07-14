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

content_units = Table(
    "content_units",
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
    Column("content_unit_id", Integer, ForeignKey("content_units.id")),
)


def start_mappers():
    mapper_registry = registry()
    mapper_registry.map_imperatively(model.ContentUnit, content_units)
    mapper_registry.map_imperatively(
        model.Digest,
        digests,
        properties={
            "content_units": relationship(
                model.ContentUnit, secondary=digest_content_association
            )
        },
    )
