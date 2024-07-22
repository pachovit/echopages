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

    def update(self, digest: model.Digest) -> None:
        pass


class FakeUnitOfWork(repositories.UnitOfWork):
    def __init__(self) -> None:
        self.content_repo = FakeContentRepository([])
        self.digest_repo = FakeDigestRepository([])
        self.committed = False

    def _commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


class FakeDigestFormatter(model.DigestFormatter):
    def format(self, digest: model.Digest) -> str:
        if digest.contents:
            return ",".join([content.text for content in digest.contents])
        else:
            raise ValueError("Digest Is Empty")


class FakeDigestDeliverySystem(model.DigestDeliverySystem):
    def __init__(self) -> None:
        super().__init__()

        self.sent_contents: List[str] = []

    def deliver_digest(self, digest_str: str) -> None:
        self.sent_contents.append(digest_str)
        logger.info(f"Sent contents {digest_str}")
