import abc
from typing import List

from echopages.domain import model


class ContentRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self, content_units: List[model.ContentUnit]):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[model.ContentUnit]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, content_unit: model.ContentUnit):
        raise NotImplementedError


class DigestRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self) -> model.Digest:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> List[model.Digest]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, digest: model.Digest) -> None:
        raise NotImplementedError
