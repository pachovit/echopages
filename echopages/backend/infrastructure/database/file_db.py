from __future__ import annotations

import json
import os
from typing import List, Optional

from echopages.backend.domain import repositories
from echopages.backend.domain.model import Content, Digest


class FileContentRepository(repositories.ContentRepository):
    """Content repository using a file to store the data as JSON."""

    def __init__(self, filepath: str) -> None:
        """Initialize the repository with the given file path.

        Args:
            filepath: The path to the file.
        """
        self.filepath = filepath

        if not os.path.exists(filepath):
            self.contents: List[Content] = []
            self.save()
        else:
            self._load()

    def _load(self) -> None:
        """Load the contents from the file."""
        with open(self.filepath, "r") as file:
            self.contents = [Content(**content) for content in json.load(file)]

    def save(self) -> None:
        """Save the contents to the file."""
        with open(self.filepath, "w") as file:
            json.dump([content.__dict__ for content in self.contents], file, indent=2)

    def get_by_id(self, content_id: int) -> Optional[Content]:
        self._load()
        for content in self.contents:
            if content.id == content_id:
                return content
        return None

    def get_all(self) -> List[Content]:
        self._load()
        return self.contents

    def add(self, content: Content) -> int:
        self._load()
        content.id = (
            max([c.__dict__.get("id", 0) for c in self.contents], default=0) + 1
        )
        self.contents.append(content)
        return content.id


class FileDigestRepository(repositories.DigestRepository):
    """Digest repository using a file to store the data as JSON."""

    def __init__(self, filepath: str):
        """Initialize the repository with the given file path.

        Args:
            filepath: The path to the file.
        """
        self.filepath = filepath

        if not os.path.exists(filepath):
            self.digests: List[Digest] = []
            self.save()
        else:
            self._load()

    def _load(self) -> None:
        """Load the digests from the file."""
        with open(self.filepath, "r") as file:
            self.digests = [
                Digest.from_dict(digest_dict) for digest_dict in json.load(file)
            ]

    def save(self) -> None:
        """Save the digests to the file."""
        with open(self.filepath, "w") as file:
            json.dump([digest.to_dict() for digest in self.digests], file, indent=2)

    def get_by_id(self, digest_id: int) -> Optional[Digest]:
        self._load()
        for digest in self.digests:
            if digest.id == digest_id:
                return digest
        return None

    def get_all(self) -> List[Digest]:
        self._load()
        return self.digests

    def add(self, digest: Digest) -> int:
        self._load()
        digest.id = (
            max([digest.to_dict().get("id", 0) for digest in self.digests], default=0)
            + 1
        )
        self.digests.append(digest)
        return digest.id

    def update(self, digest: Digest) -> None:
        self._load()
        for i, d in enumerate(self.digests):
            if d.id == digest.id:
                self.digests[i] = digest
                break


class FileUnitOfWork(repositories.UnitOfWork):
    """Unit of work using files to store the data as JSONs."""

    def __init__(self, db_path: str) -> None:
        """Initialize the unit of work with the given database path.

        Args:
            db_path: The path to the directory where the files will be stored.
        """
        super().__init__()
        os.makedirs(db_path, exist_ok=True)
        self.content_repo = FileContentRepository(
            os.path.join(db_path, "contents.json")
        )
        self.digest_repo = FileDigestRepository(os.path.join(db_path, "digests.json"))

    def __enter__(self) -> FileUnitOfWork:
        return self

    def __exit__(self, *args) -> None:  # type: ignore
        pass

    def _commit(self) -> None:
        self.content_repo: FileContentRepository
        self.digest_repo: FileDigestRepository
        self.content_repo.save()
        self.digest_repo.save()

    def rollback(self) -> None:
        pass
