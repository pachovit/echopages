import logging
from typing import List, Optional, Tuple

from echopages.backend.domain import model, repositories

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
    def format(self, contents: List[model.Content]) -> model.DigestRepr:
        if contents:
            title = "Daily Digest: " + ", ".join(
                [content.source for content in contents]
            )
            text = ",".join([str(content.__dict__) for content in contents])
            return model.DigestRepr(
                model.DigestTitle(title), model.DigestContentStr(text)
            )
        else:
            raise ValueError("Digest Is Empty")


class FakeDigestDeliverySystem(model.DigestDeliverySystem):
    def __init__(self) -> None:
        super().__init__()

        self.sent_contents: List[Tuple[model.DigestTitle, model.DigestContentStr]] = []

    def deliver_digest(self, digest_repr: model.DigestRepr) -> None:
        digest_tuple = digest_repr.title, digest_repr.contents_str
        self.sent_contents.append(digest_tuple)
        logger.info(f"Sent contents {digest_tuple}")
