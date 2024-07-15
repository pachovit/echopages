from __future__ import annotations

import abc
from typing import List, Optional

from echopages.domain import model


class ContentRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, content_id: int) -> Optional[model.Content]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[model.Content]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, content: model.Content) -> int:
        raise NotImplementedError


class DigestRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, digest_id: int) -> Optional[model.Digest]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[model.Digest]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, digest: model.Digest) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, digest: model.Digest) -> None:
        raise NotImplementedError
