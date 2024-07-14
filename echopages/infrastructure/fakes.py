import logging
from typing import List

from echopages.domain import model, repositories

logger = logging.getLogger(__name__)


class FakeContentRepository(repositories.ContentRepository):
    def __init__(self, contents: List[model.Content]):
        self.contents = contents

    def get_by_id(self, content_id: str) -> model.Content:
        return next(c for c in self.contents if c.id == content_id)

    def get_all(self) -> List[model.Content]:
        return self.contents

    def add(self, content: model.Content):
        if content.id is None:
            content.id = len(self.contents) + 1
        self.contents.append(content)


class FakeDigestRepository(repositories.DigestRepository):
    def __init__(self, digests: List[model.Digest]):
        self.digests = digests

    def get_by_id(self, digest_id: str) -> model.Digest:
        return next(d for d in self.digests if d.id == digest_id)

    def get_all(self) -> List[model.Digest]:
        return self.digests

    def add(self, digest: model.Content):
        self.digests.append(digest)


class FakeDigestDeliverySystem(model.DigestDeliverySystem):
    def __init__(self) -> None:
        super().__init__()

        self.sent_contents = []

    def deliver_digest(self, digest: model.Digest) -> None:
        content_to_send = ",".join([content.text for content in digest.contents])
        self.sent_contents.append(content_to_send)
        logger.info(f"Sent contents {content_to_send}")
