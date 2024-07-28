import abc
from dataclasses import dataclass
from typing import Callable, List, NewType, Optional


class Content:
    def __init__(
        self,
        id: Optional[int] = None,
        source: str = "",
        author: str = "",
        location: str = "",
        text: str = "",
    ) -> None:
        self.id = id
        self.text = text
        self.source = source
        self.author = author
        self.location = location


DigestTitle = NewType("DigestTitle", str)
DigestContentStr = NewType("DigestContentStr", str)


@dataclass
class DigestRepr:
    title: DigestTitle
    contents_str: DigestContentStr


class Digest:
    def __init__(
        self,
        id: Optional[int] = None,
        content_ids: List[int] = [],
        sent: bool = False,
    ) -> None:
        self.id = id
        self.content_ids = content_ids
        self.sent = sent

    def mark_as_sent(self) -> None:
        self.sent = True


class ContentSampler(abc.ABC):
    @abc.abstractmethod
    def sample(
        self, digests: List[Digest], contents: List[Content], number_of_units: int
    ) -> List[Content]:
        raise NotImplementedError


class DigestFormatter(abc.ABC):
    @abc.abstractmethod
    def format(self, contents: List[Content]) -> DigestRepr:
        raise NotImplementedError


class DigestDeliverySystem(abc.ABC):
    @abc.abstractmethod
    def deliver_digest(self, digest_repr: DigestRepr) -> None:
        raise NotImplementedError


class Scheduler(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        function: Callable[[], None],
        time_of_day: Optional[str] = None,
        time_zone: str = "Europe/Berlin",
        sleep_interval: float = 1.0,
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def configure_schedule(self, time_of_day: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
