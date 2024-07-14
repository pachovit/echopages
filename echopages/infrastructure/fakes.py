import logging
from typing import List, Optional

from echopages.domain import model, repositories

logger = logging.getLogger(__name__)


class FakeContentRepository(repositories.ContentRepository):
    def __init__(self, contents: List[model.Content]) -> None:
        self.contents = contents

    def get_by_id(self, content_id: int) -> model.Content:
        return next(c for c in self.contents if c.id == content_id)

    def get_all(self) -> List[model.Content]:
        return self.contents

    def add(self, content: model.Content) -> int:
        if content.id is None:
            content.id = len(self.contents) + 1
        self.contents.append(content)
        return content.id


class FakeDigestRepository(repositories.DigestRepository):
    def __init__(self, digests: List[model.Digest]) -> None:
        self.digests = digests

    def get_by_id(self, digest_id: int) -> Optional[model.Digest]:
        try:
            return next(d for d in self.digests if d.id == digest_id)
        except StopIteration:
            return None

    def get_all(self) -> List[model.Digest]:
        return self.digests

    def add(self, digest: model.Digest) -> int:
        if digest.id is None:
            digest.id = len(self.digests) + 1
        self.digests.append(digest)
        return digest.id


class FakeDigestDeliverySystem(model.DigestDeliverySystem):
    def __init__(self) -> None:
        super().__init__()

        self.sent_contents: List[str] = []

    def deliver_digest(self, digest: model.Digest) -> None:
        if digest.contents:
            content_to_send = ",".join([content.text for content in digest.contents])
        else:
            raise ValueError("Digest Is Empty")
        self.sent_contents.append(content_to_send)
        logger.info(f"Sent contents {content_to_send}")
