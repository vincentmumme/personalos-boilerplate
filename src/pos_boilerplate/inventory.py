from __future__ import annotations

import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .policy import Classification, ExportPolicy, PolicyError


class InventoryError(RuntimeError):
    """Raised when the source repository cannot be inventoried."""


@dataclass(frozen=True)
class InventoryResult:
    files: tuple[Classification, ...]
    unclassified: list[str]
    counts: dict[str, int]

    @property
    def ok(self) -> bool:
        return not self.unclassified

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "counts": self.counts,
            "unclassified": self.unclassified,
            "files": [
                {
                    "path": item.path,
                    "rule_id": item.rule_id,
                    "action": item.action,
                    "reason": item.reason,
                    **({"target": item.target} if item.target else {}),
                    **({"module": item.module} if item.module else {}),
                }
                for item in self.files
            ],
        }


def git_tracked_files(source: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(source), "ls-files", "-z"],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise InventoryError(f"Cannot inventory Git repository {source}: {exc}") from exc
    return sorted(
        path.decode("utf-8")
        for path in completed.stdout.split(b"\0")
        if path
    )


def git_committed_files(source: Path, revision: str) -> list[str]:
    """Return the exact tree recorded by one immutable Git revision."""

    try:
        completed = subprocess.run(
            ["git", "-C", str(source), "ls-tree", "-r", "-z", "--name-only", revision],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise InventoryError(
            f"Cannot inventory Git revision {revision} in {source}: {exc}"
        ) from exc
    return sorted(path.decode("utf-8") for path in completed.stdout.split(b"\0") if path)


def inventory(paths: Iterable[str], policy: ExportPolicy) -> InventoryResult:
    classified: list[Classification] = []
    unclassified: list[str] = []
    for path in sorted(set(paths)):
        try:
            classified.append(policy.classify(path))
        except PolicyError:
            unclassified.append(path)
    counts = dict(sorted(Counter(item.action for item in classified).items()))
    return InventoryResult(tuple(classified), unclassified, counts)
