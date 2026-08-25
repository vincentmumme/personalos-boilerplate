from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


ALLOWED_ACTIONS = {"copy", "render", "module", "fixture", "exclude"}
MODULE_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class PolicyError(ValueError):
    """Raised when an export policy is invalid or incomplete."""


@dataclass(frozen=True)
class PolicyRule:
    id: str
    pattern: str
    action: str
    reason: str
    target: str | None = None
    module: str | None = None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "PolicyRule":
        required = ("id", "pattern", "action", "reason")
        missing = [key for key in required if not isinstance(data.get(key), str) or not data[key].strip()]
        if missing:
            raise PolicyError(f"Policy rule is missing non-empty fields: {', '.join(missing)}")
        if data["action"] not in ALLOWED_ACTIONS:
            raise PolicyError(
                f"Unsupported action {data['action']!r}; expected one of {sorted(ALLOWED_ACTIONS)}"
            )
        if data["action"] == "module" and not data.get("module"):
            raise PolicyError(f"Module rule {data['id']!r} requires a module name")
        target = data.get("target")
        if target is not None and (
            not isinstance(target, str) or not _is_safe_relative_path(target)
        ):
            raise PolicyError(f"Policy rule {data['id']!r} has an unsafe target")
        module = data.get("module")
        if module is not None and (
            not isinstance(module, str) or MODULE_RE.fullmatch(module) is None
        ):
            raise PolicyError(f"Policy rule {data['id']!r} has an unsafe module name")
        return cls(
            id=data["id"],
            pattern=data["pattern"],
            action=data["action"],
            reason=data["reason"],
            target=target,
            module=module,
        )

    def matches(self, normalized_path: str) -> bool:
        return fnmatch.fnmatchcase(normalized_path, self.pattern)


@dataclass(frozen=True)
class Classification:
    path: str
    rule_id: str
    action: str
    reason: str
    target: str | None = None
    module: str | None = None


@dataclass(frozen=True)
class ExportPolicy:
    schema_version: int
    rules: tuple[PolicyRule, ...]

    @classmethod
    def load(cls, path: Path) -> "ExportPolicy":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PolicyError(f"Cannot load export policy {path}: {exc}") from exc
        return cls.from_data(data)

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "ExportPolicy":
        if data.get("schema_version") != 1:
            raise PolicyError("Export policy schema_version must be 1")
        raw_rules = data.get("rules")
        if not isinstance(raw_rules, list) or not raw_rules:
            raise PolicyError("Export policy requires a non-empty rules list")
        rules = tuple(PolicyRule.from_data(item) for item in raw_rules)
        ids = [rule.id for rule in rules]
        if len(ids) != len(set(ids)):
            raise PolicyError("Export policy rule ids must be unique")
        return cls(schema_version=1, rules=rules)

    def classify(self, relative_path: str) -> Classification:
        normalized = PurePosixPath(relative_path).as_posix()
        for rule in self.rules:
            if rule.matches(normalized):
                return Classification(
                    path=normalized,
                    rule_id=rule.id,
                    action=rule.action,
                    reason=rule.reason,
                    target=rule.target,
                    module=rule.module,
                )
        raise PolicyError(f"Unclassified source path: {normalized}")


def _is_safe_relative_path(value: str) -> bool:
    if not value or value in {".", ".."} or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts
