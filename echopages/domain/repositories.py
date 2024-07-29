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


class UnitOfWork(abc.ABC):
    """
    Abstract base class for a unit of work.

    A unit of work is a transactional object that represents a single logical
    unit of work. It is used to encapsulate the business logic that needs to
    be executed in a single transaction.

    The unit of work is responsible for managing the state of the repositories
    and ensuring that the changes are committed atomically.

    Example usage:
    ```
    with uow:
        # Do some business logic
        digest = uow.digest_repo.get_by_id(1)
        digest.content_ids.append(2)
    ```

    Attributes:
        content_repo: The content repository.
        digest_repo: The digest repository.
    """

    content_repo: ContentRepository
    digest_repo: DigestRepository

    def __enter__(self) -> UnitOfWork:
        """
        Enter the unit of work.
        """
        return self

    def __exit__(self, *args) -> None:  # type: ignore
        """
        Exit the unit of work.

        If an exception is raised during the execution of the unit of work,
        the changes are rolled back.
        """
        self.rollback()

    def commit(self) -> None:
        """
        Commit the changes made in the unit of work.

        This method should be called after all the changes have been made to
        the repositories. It will commit the changes atomically.
        """
        self._commit()

    @abc.abstractmethod
    def _commit(self) -> None:
        """
        Commit the changes made in the unit of work.

        This method should be implemented by subclasses to provide the
        functionality to commit the changes made in the unit of work.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """
        Rollback the changes made in the unit of work.

        This method should be implemented by subclasses to provide the
        functionality to rollback the changes made in the unit of work.
        """
        raise NotImplementedError
