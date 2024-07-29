import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, NewType, Optional


@dataclass
class Content:
    """
    A Content unit.

    Attributes:
        id: The ID of the content item.
        source: The source of the content item. E.g. book name, or article name.
        author: The author of the content item.
        location: The location of the content item. E.g. chapter 1, section 1.1, or page 75.
        text: The actual content.
    """

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
    """
    A representation of a Digest.
    """

    title: DigestTitle
    contents_str: DigestContentStr


class Digest:
    """
    A Digest is a collection of content items that is sent out to the user.

    Attributes:
        id: The ID of the Digest.
        content_ids: The IDs of the Content items included in the Digest.
        sent_at: The time the Digest was sent.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        content_ids: List[int] = [],
        sent_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.content_ids = content_ids
        self.sent_at = sent_at

    def mark_as_sent(self) -> None:
        """
        Mark the Digest as sent, setting the sent_at attribute to the current time.
        """
        self.sent_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Digest to a dictionary representation.
        """
        sent_at = self.sent_at.isoformat() if self.sent_at else None
        return {"id": self.id, "content_ids": self.content_ids, "sent_at": sent_at}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Digest":
        """
        Create a Digest object from a dictionary representation.
        """
        return cls(
            id=data["id"],
            content_ids=data["content_ids"],
            sent_at=datetime.fromisoformat(data["sent_at"])
            if data["sent_at"]
            else None,
        )


class ContentSampler(abc.ABC):
    """
    Abstract base class for Content Samplers. Content Samplers are used to
    choose which content units to include in a Digest.
    """

    @abc.abstractmethod
    def sample(
        self, digests: List[Digest], contents: List[Content], number_of_units: int
    ) -> List[Content]:
        """
        Sample a given number of Contents, from the previous Digests and the available Contents.

        Args:
            digests: The digests to sample from.
            contents: The contents to sample from.
            number_of_units: The number of units to sample.

        Returns:
            The sampled contents.
        """
        raise NotImplementedError


class DigestFormatter(abc.ABC):
    """
    Abstract base class for digest formatters. Digest formatters are used to
    format some contents into a digest representation.
    """

    @abc.abstractmethod
    def format(self, contents: List[Content]) -> DigestRepr:
        """
        Format the given contents into a Digest Representation.

        Args:
            contents: The contents to format.

        Returns:
            The formatted digest representation.
        """
        raise NotImplementedError


class DigestDeliverySystem(abc.ABC):
    """
    Abstract base class for digest delivery systems. Digest delivery systems
    are used to deliver digests to the user.
    """

    @abc.abstractmethod
    def deliver_digest(self, digest_repr: DigestRepr) -> None:
        """
        Deliver the given digest representation.

        Args:
            digest_repr: The digest representation to deliver.
        """
        raise NotImplementedError


class Scheduler(abc.ABC):
    """
    Abstract base class for schedulers. Schedulers are used to schedule
    the execution of any function at a given time of day.
    """

    @abc.abstractmethod
    def __init__(
        self,
        function: Callable[[], None],
        time_of_day: Optional[str] = None,
        time_zone: str = "Europe/Berlin",
        sleep_interval: float = 1.0,
    ) -> None:
        """
        Initializes a Scheduler object.

        Args:
            function: The function to be scheduled.
            time_of_day: The time of day to schedule the function. Defaults to None.
            time_zone: The time zone to use. Defaults to "Europe/Berlin".
            sleep_interval : The sleep interval to wait to see if the time to trigger has arrived. Defaults to 1.0.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def configure_schedule(self, time_of_day: str) -> None:
        """
        Configure the schedule for the given time of day.

        Args:
            time_of_day: The time of day to schedule the function.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def start(self) -> None:
        """
        Start the scheduler.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self) -> None:
        """
        Stop the scheduler.
        """
        raise NotImplementedError
