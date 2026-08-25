#!/usr/bin/env python3
"""Resolve PersonalOS local time without depending on the host timezone."""

from __future__ import annotations

import os
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ENV_TIMEZONE = "PERSONALOS_TIMEZONE"
TRUTH_SYSTEM_PATH = Path("system/truth-systems/personalos.md")
FRONTMATTER_RE = re.compile(r"^default_timezone:\s*[\"']?([^\"'\n]+)[\"']?\s*$", re.MULTILINE)


def _validated_timezone(value: str, *, source: str) -> ZoneInfo:
    candidate = value.strip()
    try:
        return ZoneInfo(candidate)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(f"Invalid IANA timezone from {source}: {candidate!r}") from exc


def instance_default_timezone(root: Path) -> ZoneInfo:
    path = root / TRUTH_SYSTEM_PATH
    if not path.is_file():
        raise ValueError(f"PersonalOS timezone owner is missing: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"PersonalOS timezone owner has no frontmatter: {path}")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError(f"PersonalOS timezone owner has malformed frontmatter: {path}")
    match = FRONTMATTER_RE.search(text[4:end])
    if not match:
        raise ValueError(f"PersonalOS timezone owner has no default_timezone: {path}")
    return _validated_timezone(match.group(1), source=str(path))


def resolve_timezone(root: Path, explicit: str | None = None) -> ZoneInfo:
    if explicit:
        return _validated_timezone(explicit, source="explicit context")
    environment = os.environ.get(ENV_TIMEZONE)
    if environment:
        return _validated_timezone(environment, source=ENV_TIMEZONE)
    return instance_default_timezone(root)


def local_now(root: Path, explicit: str | None = None) -> datetime:
    return datetime.now(resolve_timezone(root, explicit))


def local_date(root: Path, explicit: str | None = None) -> date:
    return local_now(root, explicit).date()
