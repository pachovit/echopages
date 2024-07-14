import logging
from typing import List

from echopages.domain import model, repositories

logger = logging.getLogger(__name__)


class FakeContentRepository(repositories.ContentRepository):
    def __init__(self, content_units: List[model.ContentUnit]):
        self.content_units = content_units

    def get_by_id(self, content_unit_id: str) -> model.ContentUnit:
        return next(c for c in self.content_units if c.id == content_unit_id)

    def get_all(self) -> List[model.ContentUnit]:
        return self.content_units

    def add(self, content_unit: model.ContentUnit):
        if content_unit.id is None:
            content_unit.id = len(self.content_units) + 1
        self.content_units.append(content_unit)


class FakeDigestRepository(repositories.DigestRepository):
    def __init__(self, digests: List[model.Digest]):
        self.digests = digests

    def get_by_id(self, digest_id: str) -> model.Digest:
        return next(d for d in self.digests if d.id == digest_id)

    def get_all(self) -> List[model.Digest]:
        return self.digests

    def add(self, digest: model.ContentUnit):
        self.digests.append(digest)


class FakeDigestDeliverySystem(model.DigestDeliverySystem):
    def __init__(self) -> None:
        super().__init__()

        self.sent_contents = []

    def deliver_digest(self, digest: model.Digest) -> None:
        content_to_send = ",".join([content.text for content in digest.content_units])
        self.sent_contents.append(content_to_send)
        logger.info(f"Sent contents {content_to_send}")
