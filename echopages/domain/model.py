import abc
import datetime
from dataclasses import dataclass, field
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


@dataclass
class Schedule:
    days_of_week: List[int]  # Monday=0, Sunday=6
    time_of_day_str: str
    time_of_day: datetime.time = field(init=False)

    def __post_init__(self):
        self.time_of_day = self.parse_time(self.time_of_day_str)
        # Validate days_of_week to ensure no invalid days are set
        if any(day < 0 or day > 6 for day in self.days_of_week):
            raise ValueError(
                "days_of_week must be integers from 0 (Monday) to 6 (Sunday)."
            )

    @staticmethod
    def parse_time(time_str: str) -> datetime.time:
        """Parse a time string in HH:MM format to a datetime.time object."""
        return datetime.datetime.strptime(time_str, "%H:%M").time()


class Scheduler(abc.ABC):
    def __init__(
        self, function: Callable[[], None], schedule: Optional[Schedule] = None
    ) -> None:
        if schedule is None:
            schedule = Schedule(
                days_of_week=[0, 1, 2, 3, 4, 5, 6], time_of_day_str="00:00"
            )
        self.schedule = schedule
        self.function = function

    def configure_schedule(self, schedule: str) -> None:
        self.schedule = schedule

    @abc.abstractmethod
    def start(self) -> None:
        raise NotImplementedError
