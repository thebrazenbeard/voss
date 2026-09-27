from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class ReviewFreshness(str, Enum):
    CURRENT = "CURRENT"
    SUPERSEDED = "SUPERSEDED"


class MutationGate(str, Enum):
    ALLOWED = "ALLOWED"
    STALE_HEAD = "STALE_HEAD"
    STALE_BLOB = "STALE_BLOB"


@dataclass(frozen=True)
class RepositorySnapshot:
    repository: str
    ref: str
    head_sha: str
    retrieved_at: str


@dataclass(frozen=True)
class ReviewBinding:
    repository: str
    ref: str
    reviewed_head_sha: str


def check_review_freshness(
    binding: ReviewBinding,
    snapshot: RepositorySnapshot,
) -> ReviewFreshness:
    if (
        binding.repository != snapshot.repository
        or binding.ref != snapshot.ref
    ):
        return ReviewFreshness.SUPERSEDED

    return (
        ReviewFreshness.CURRENT
        if binding.reviewed_head_sha == snapshot.head_sha
        else ReviewFreshness.SUPERSEDED
    )


def mutation_gate(
    *,
    expected_head: str,
    actual_head: str,
    expected_blob: str | None = None,
    actual_blob: str | None = None,
) -> MutationGate:
    if expected_head != actual_head:
        return MutationGate.STALE_HEAD

    if (
        expected_blob is not None
        and expected_blob != actual_blob
    ):
        return MutationGate.STALE_BLOB

    return MutationGate.ALLOWED


class GitReadAdapter:
    """Provider-independent Git repository evidence adapter."""

    def __init__(
        self,
        *,
        read_ref: Callable[[str, str], str],
        read_file: Callable[[str, str, str], tuple[str, str]],
    ):
        self._read_ref = read_ref
        self._read_file = read_file

    def snapshot(
        self,
        repository: str,
        ref: str,
        retrieved_at: str,
    ) -> RepositorySnapshot:
        return RepositorySnapshot(
            repository=repository,
            ref=ref,
            head_sha=self._read_ref(repository, ref),
            retrieved_at=retrieved_at,
        )

    def read_exact_file(
        self,
        repository: str,
        path: str,
        ref: str,
    ) -> tuple[str, str]:
        return self._read_file(repository, path, ref)
