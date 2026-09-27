from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from voss_core.case import (
    CurrentnessStatus,
    EpistemicStatus,
    EvidenceFidelity,
    EvidenceOrigin,
    EvidenceRecord,
)
from voss_core.repository import RepositorySnapshot


class GitHubLiveError(RuntimeError):
    pass


@dataclass(frozen=True)
class LiveBranchRead:
    repository: str
    ref: str
    head_sha: str
    retrieved_at: str


@dataclass(frozen=True)
class LiveFileRead:
    repository: str
    requested_ref: str
    bound_head_sha: str
    path: str
    blob_sha: str
    content: str
    retrieved_at: str
    ref_stable_after_read: bool
    postread_head_sha: str


@dataclass(frozen=True)
class LiveCompareRead:
    repository: str
    base_sha: str
    head_sha: str
    status: str
    ahead_by: int
    behind_by: int
    files: tuple[tuple[str, str], ...]
    retrieved_at: str


class GitHubRESTClient:
    """Read-only live GitHub evidence adapter.

    Mutable refs are read first, file contents are fetched by exact
    commit SHA, and the mutable ref is read again after the file read.
    This prevents branch movement from being silently mixed into one
    evidence observation.
    """

    def __init__(
        self,
        token: str | None = None,
        api_base: str = "https://api.github.com",
    ):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_base = api_base.rstrip("/")

    def _get_json(
        self,
        path: str,
        params: dict | None = None,
    ):
        url = self.api_base + path
        if params:
            url += "?" + urlencode(params)

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "voss-forensic-auditor",
        }
        if self.token:
            headers["Authorization"] = (
                f"Bearer {self.token}"
            )

        request = Request(
            url,
            headers=headers,
            method="GET",
        )

        try:
            with urlopen(
                request,
                timeout=30,
            ) as response:
                return json.loads(
                    response.read().decode("utf-8")
                )
        except Exception as exc:
            raise GitHubLiveError(
                f"GitHub read failed for {url}: {exc}"
            ) from exc

    def read_branch(
        self,
        repository: str,
        ref: str,
        retrieved_at: str,
    ) -> LiveBranchRead:
        encoded = quote(
            f"heads/{ref}",
            safe="",
        )
        payload = self._get_json(
            f"/repos/{repository}/git/ref/{encoded}"
        )
        sha = payload["object"]["sha"]
        return LiveBranchRead(
            repository,
            ref,
            sha,
            retrieved_at,
        )

    def read_file(
        self,
        repository: str,
        path: str,
        ref: str,
        retrieved_at: str,
    ) -> LiveFileRead:
        before = self.read_branch(
            repository,
            ref,
            retrieved_at,
        )

        payload = self._get_json(
            (
                f"/repos/{repository}/contents/"
                f"{quote(path, safe='/')}"
            ),
            {"ref": before.head_sha},
        )

        if payload.get("type") != "file":
            raise GitHubLiveError(
                f"{repository}:{path} is not a file"
            )

        if payload.get("encoding") != "base64":
            raise GitHubLiveError(
                "unsupported GitHub content encoding"
            )

        content = base64.b64decode(
            payload["content"]
        ).decode("utf-8")

        after = self.read_branch(
            repository,
            ref,
            retrieved_at,
        )

        return LiveFileRead(
            repository=repository,
            requested_ref=ref,
            bound_head_sha=before.head_sha,
            path=path,
            blob_sha=payload["sha"],
            content=content,
            retrieved_at=retrieved_at,
            ref_stable_after_read=(
                before.head_sha == after.head_sha
            ),
            postread_head_sha=after.head_sha,
        )

    def compare(
        self,
        repository: str,
        base_sha: str,
        head_sha: str,
        retrieved_at: str,
    ) -> LiveCompareRead:
        payload = self._get_json(
            (
                f"/repos/{repository}/compare/"
                f"{base_sha}...{head_sha}"
            )
        )

        return LiveCompareRead(
            repository=repository,
            base_sha=base_sha,
            head_sha=head_sha,
            status=payload["status"],
            ahead_by=int(payload["ahead_by"]),
            behind_by=int(payload["behind_by"]),
            files=tuple(
                (
                    item["filename"],
                    item["status"],
                )
                for item in payload.get(
                    "files",
                    [],
                )
            ),
            retrieved_at=retrieved_at,
        )


def branch_snapshot(
    read: LiveBranchRead,
) -> RepositorySnapshot:
    return RepositorySnapshot(
        repository=read.repository,
        ref=read.ref,
        head_sha=read.head_sha,
        retrieved_at=read.retrieved_at,
    )


def file_evidence(
    read: LiveFileRead,
    *,
    evidence_id: str,
    subject_id: str,
    proposition: str,
    supports: tuple[str, ...] = (),
    contradicts: tuple[str, ...] = (),
    independence_group: str | None = None,
) -> EvidenceRecord:
    limitations: tuple[str, ...] = ()
    currentness = CurrentnessStatus.CURRENT

    if not read.ref_stable_after_read:
        limitations = (
            "mutable ref moved during read; content remains "
            "exact for bound_head_sha but is not current-ref "
            "evidence",
        )
        currentness = CurrentnessStatus.STALE

    return EvidenceRecord(
        id=evidence_id,
        source_ref=(
            f"github://{read.repository}@"
            f"{read.bound_head_sha}/{read.path}"
        ),
        subject_id=subject_id,
        proposition=proposition,
        origin=EvidenceOrigin.PRIMARY_SOURCE,
        fidelity=EvidenceFidelity.EXACT_UTF8_SPAN,
        epistemic_status=EpistemicStatus.OBSERVED,
        currentness=currentness,
        immutable_ref=f"git-blob:{read.blob_sha}",
        retrieval_time=read.retrieved_at,
        independence_group=independence_group,
        supports=supports,
        contradicts=contradicts,
        limitations=limitations,
    )
