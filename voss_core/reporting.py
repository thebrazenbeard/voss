from __future__ import annotations

from collections import Counter


class ReportConsistencyError(ValueError):
    pass


def summarize_verdicts(
    cases: list[dict],
) -> dict[str, int]:
    counts: Counter[str] = Counter()

    for case in cases:
        for claim in case.get(
            "claims",
            [],
        ):
            verdict = claim.get(
                "verdict"
            )
            if verdict:
                counts[str(verdict)] += 1

    return {
        key: counts.get(key, 0)
        for key in (
            "PASS",
            "FAIL",
            "UNRESOLVED",
            "BLOCKED",
            "CONFLICT",
            "OUTCOME_UNKNOWN",
            "NOT_APPLICABLE",
        )
    }


def verify_report_counts(
    report: dict,
    cases: list[dict],
) -> None:
    actual = summarize_verdicts(
        cases
    )

    declared = {
        key: int(
            report.get(
                "finding_counts",
                {},
            ).get(
                key,
                0,
            )
        )
        for key in actual
    }

    if declared != actual:
        raise ReportConsistencyError(
            "report finding_counts do not match "
            f"case corpus: declared={declared}, "
            f"actual={actual}"
        )
