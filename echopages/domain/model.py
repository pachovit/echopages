import abc
from typing import Callable, List, Optional


class ContentUnit:
    def __init__(self, id: Optional[int] = None, text: str = "") -> None:
        self.id = id
        self.text = text


class Digest:
    def __init__(
        self,
        id: Optional[int] = None,
        content_units: Optional[List[ContentUnit]] = [],
        sent: Optional[bool] = False,
    ) -> None:
        self.id = id
        self.content_units = content_units
        self.sent = sent

    def mark_as_sent(self):
        self.sent = True


class ContentSampler(abc.ABC):
    @abc.abstractmethod
    def sample(
        self, content_units: List[ContentUnit], number_of_units: int
    ) -> List[ContentUnit]:
        raise NotImplementedError


class DigestDeliverySystem(abc.ABC):
    @abc.abstractmethod
    def deliver_digest(self, digest: Digest) -> None:
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
        pass

    @abc.abstractmethod
    def configure_schedule(self, time_of_day: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
