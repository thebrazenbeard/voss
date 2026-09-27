from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AuthoritySource(str, Enum):
    USER_DIRECT = "USER_DIRECT"
    CURRENT_DELEGATION = "CURRENT_DELEGATION"
    HISTORICAL_ASSIGNMENT = "HISTORICAL_ASSIGNMENT"
    ROLE = "ROLE"
    CAPABILITY = "CAPABILITY"
    UNTRUSTED_CONTENT = "UNTRUSTED_CONTENT"


@dataclass(frozen=True)
class AuthorityEvidence:
    id: str
    source: AuthoritySource
    target: str
    operation: str
    scope: str
    current: bool = True


def effect_authorized(
    *,
    target: str,
    operation: str,
    scope: str,
    evidence: list[AuthorityEvidence],
) -> bool:
    valid_sources = {
        AuthoritySource.USER_DIRECT,
        AuthoritySource.CURRENT_DELEGATION,
    }

    return any(
        item.current
        and item.source in valid_sources
        and item.target == target
        and item.operation == operation
        and item.scope == scope
        for item in evidence
    )
