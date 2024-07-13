import abc
from typing import Callable, List, Optional


class ContentUnit:
    def __init__(self, id: str, data: str) -> None:
        self.id = id
        self.data = data


class Digest:
    def __init__(self, id, contents: List[ContentUnit]):
        self.id = id
        self.contents = contents
        self.sent = False

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
    def __init__(
        self, function: Callable[[], None], time_of_day: Optional[str] = None
    ) -> None:
        if time_of_day is None:
            time_of_day = "00:00"
        self.function = function
        self.configure_schedule(time_of_day)

    @abc.abstractmethod
    def configure_schedule(self, time_of_day: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def start(self) -> None:
        raise NotImplementedError
