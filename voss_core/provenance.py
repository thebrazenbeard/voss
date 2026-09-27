from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class ProvenanceRelation(str, Enum):
    LITERAL = "LITERAL"
    REFERENTIAL = "REFERENTIAL"
    ANCESTRAL = "ANCESTRAL"
    ORIGIN_CLAIM = "ORIGIN_CLAIM"
    OTHER = "OTHER"


@dataclass(frozen=True, order=True)
class TimeInterval:
    start: datetime
    end: datetime

    def definitely_before(self, other: "TimeInterval") -> bool:
        return self.end < other.start

    def overlaps(self, other: "TimeInterval") -> bool:
        return not (
            self.definitely_before(other)
            or other.definitely_before(self)
        )


def _utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_time_interval(value: str) -> TimeInterval:
    value = value.strip()

    if len(value) == 7 and value[4] == "-":
        year, month = map(int, value.split("-"))
        last = calendar.monthrange(year, month)[1]
        return TimeInterval(
            datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc),
            datetime(year, month, last, 23, 59, 59, 999999, tzinfo=timezone.utc),
        )

    if len(value) == 10 and value[4] == "-" and value[7] == "-":
        dt = datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
        return TimeInterval(
            dt,
            dt.replace(hour=23, minute=59, second=59, microsecond=999999),
        )

    normalized = value.replace("Z", "+00:00")
    dt = _utc(datetime.fromisoformat(normalized))
    return TimeInterval(dt, dt)


@dataclass(frozen=True)
class ProvenanceCandidate:
    id: str
    event_time: TimeInterval
    relation: ProvenanceRelation
    references: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProvenanceTrace:
    earliest_accessible: tuple[str, ...]
    first_literal: tuple[str, ...]
    conceptual_ancestors: tuple[str, ...]
    origin_claims: tuple[str, ...]
    unresolved_backrefs: tuple[str, ...]


def _earliest_band(records: list[ProvenanceCandidate]) -> tuple[str, ...]:
    if not records:
        return ()

    earliest = []
    for candidate in records:
        if not any(
            other.event_time.definitely_before(candidate.event_time)
            for other in records
            if other.id != candidate.id
        ):
            earliest.append(candidate.id)
    return tuple(sorted(earliest))


def trace_provenance(
    records: list[ProvenanceCandidate],
) -> ProvenanceTrace:
    ids = {record.id for record in records}
    literals = [
        record
        for record in records
        if record.relation == ProvenanceRelation.LITERAL
    ]

    unresolved = sorted(
        {
            ref
            for record in records
            for ref in record.references
            if ref not in ids
        }
    )

    return ProvenanceTrace(
        earliest_accessible=_earliest_band(records),
        first_literal=_earliest_band(literals),
        conceptual_ancestors=tuple(
            record.id
            for record in sorted(
                records,
                key=lambda item: item.event_time.start,
            )
            if record.relation == ProvenanceRelation.ANCESTRAL
        ),
        origin_claims=tuple(
            record.id
            for record in sorted(
                records,
                key=lambda item: item.event_time.start,
            )
            if record.relation == ProvenanceRelation.ORIGIN_CLAIM
        ),
        unresolved_backrefs=tuple(unresolved),
    )


def requires_chronology_restart(
    interpreted_frontier: TimeInterval,
    newly_discovered: TimeInterval,
) -> bool:
    return newly_discovered.definitely_before(interpreted_frontier)
