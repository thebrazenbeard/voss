import base64
import unittest

from voss_adapters.github_live import (
    GitHubRESTClient,
    file_evidence,
)
from voss_core.case import (
    CurrentnessStatus,
    PropositionType,
)
from voss_core.multisubject import (
    CrossSubjectClaim,
    MultiSubjectCaseFile,
    SubjectBinding,
    SubjectKind,
)
from voss_core.reporting import (
    ReportConsistencyError,
    summarize_verdicts,
    verify_report_counts,
)


class FakeGitHub(GitHubRESTClient):
    def __init__(self):
        self.calls = 0
        self.api_base = "fake"
        self.token = None

    def _get_json(
        self,
        path,
        params=None,
    ):
        if "/git/ref/" in path:
            self.calls += 1
            return {
                "object": {
                    "sha": (
                        "aaa"
                        if self.calls == 1
                        else "bbb"
                    )
                }
            }

        return {
            "type": "file",
            "sha": "blob1",
            "encoding": "base64",
            "content": base64.b64encode(
                b"hello"
            ).decode("ascii"),
        }


class RealProjectRegressionTests(unittest.TestCase):
    def test_branch_movement_marks_file_stale(self):
        client = FakeGitHub()

        read = client.read_file(
            "owner/repo",
            "README.md",
            "main",
            "2026-09-20T00:00:00Z",
        )

        self.assertFalse(
            read.ref_stable_after_read
        )

        evidence = file_evidence(
            read,
            evidence_id="e1",
            subject_id="s1",
            proposition="source text",
        )

        self.assertEqual(
            evidence.currentness,
            CurrentnessStatus.STALE,
        )
        self.assertEqual(
            evidence.immutable_ref,
            "git-blob:blob1",
        )

    def test_multisubject_case_supports_cross_ref_claim(self):
        case = MultiSubjectCaseFile(
            case_id="case",
            literal_task="compare refs",
            source_frontier="cut",
            subjects=(
                SubjectBinding(
                    "main",
                    SubjectKind.REPOSITORY_REF,
                    "repo@main",
                    "a",
                    True,
                ),
                SubjectBinding(
                    "feature",
                    SubjectKind.REPOSITORY_REF,
                    "repo@feature",
                    "b",
                    True,
                ),
            ),
            claims=(
                CrossSubjectClaim(
                    "cmp",
                    ("main", "feature"),
                    "feature differs from main",
                    PropositionType.FACT,
                ),
            ),
            evidence=(),
        ).validate()

        self.assertEqual(
            len(case.subjects),
            2,
        )

    def test_report_counts_are_derived_from_cases(self):
        cases = [
            {
                "claims": [
                    {"verdict": "PASS"},
                    {"verdict": "FAIL"},
                ]
            },
            {
                "claims": [
                    {"verdict": "UNRESOLVED"},
                    {"verdict": "FAIL"},
                ]
            },
        ]

        counts = summarize_verdicts(
            cases
        )

        self.assertEqual(
            counts["PASS"],
            1,
        )
        self.assertEqual(
            counts["FAIL"],
            2,
        )
        self.assertEqual(
            counts["UNRESOLVED"],
            1,
        )

        with self.assertRaises(
            ReportConsistencyError
        ):
            verify_report_counts(
                {
                    "finding_counts": {
                        "PASS": 2,
                        "FAIL": 1,
                        "UNRESOLVED": 1,
                    }
                },
                cases,
            )


if __name__ == "__main__":
    unittest.main()
