import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, NewType, Optional


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
        sent_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.content_ids = content_ids
        self.sent_at = sent_at

    def mark_as_sent(self) -> None:
        self.sent_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        sent_at = self.sent_at.isoformat() if self.sent_at else None
        return {"id": self.id, "content_ids": self.content_ids, "sent_at": sent_at}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Digest":
        return cls(
            id=data["id"],
            content_ids=data["content_ids"],
            sent_at=datetime.fromisoformat(data["sent_at"])
            if data["sent_at"]
            else None,
        )


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
