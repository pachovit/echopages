import abc
from typing import List

from echopages.domain import model


class ContentRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, content_unit_id: str) -> model.ContentUnit:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[model.ContentUnit]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, content_unit: model.ContentUnit) -> int:
        raise NotImplementedError


class DigestRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self) -> model.Digest:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[model.Digest]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, digest: model.Digest) -> int:
        raise NotImplementedError
