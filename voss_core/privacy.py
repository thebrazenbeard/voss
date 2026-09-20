from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PrivacyItem:
    id: str
    private: bool
    relevant_to_claim: bool
    minimum_needed: bool = True


def admissible_for_case(
    items: list[PrivacyItem],
) -> tuple[str, ...]:
    return tuple(
        item.id
        for item in items
        if item.relevant_to_claim
        and item.minimum_needed
    )
