import abc
from typing import Callable, List, Optional


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


class Digest:
    def __init__(
        self,
        id: Optional[int] = None,
        content_ids: List[int] = [],
        sent: bool = False,
        contents_str: str = "",
    ) -> None:
        self.id = id
        self.content_ids = content_ids
        self.sent = sent
        self.contents_str = contents_str

    def mark_as_sent(self) -> None:
        self.sent = True

    def store_content_str(self, content_str: str) -> None:
        self.contents_str = content_str


class ContentSampler(abc.ABC):
    @abc.abstractmethod
    def sample(
        self, digests: List[Digest], contents: List[Content], number_of_units: int
    ) -> List[Content]:
        raise NotImplementedError


class DigestFormatter(abc.ABC):
    @abc.abstractmethod
    def format(self, contents: List[Content]) -> str:
        raise NotImplementedError


class DigestDeliverySystem(abc.ABC):
    @abc.abstractmethod
    def deliver_digest(self, digest_str: str) -> None:
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
