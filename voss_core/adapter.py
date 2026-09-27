from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from .types import Claim, Evidence, Finding


@dataclass(frozen=True)
class ProjectSnapshot:
    project_id: str
    source_frontier: str
    mutable_frontier: str | None = None
    authority_scope: str | None = None
    notes: str | None = None


class ProjectAdapter(ABC):
    """Project-specific evidence acquisition only.

    Adapters may normalize sources into Voss evidence objects.

    They must not silently change Voss verdict rules or promote historical,
    derived, claimed, or receipt evidence into a stronger evidence class.
    """

    @abstractmethod
    def snapshot(self) -> ProjectSnapshot:
        raise NotImplementedError

    @abstractmethod
    def collect_evidence(
        self,
        claims: Iterable[Claim],
    ) -> list[Evidence]:
        raise NotImplementedError

    def preflight(self) -> list[Finding]:
        return []
