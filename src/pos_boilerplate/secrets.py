from __future__ import annotations

import hashlib
import hmac
import os
import re
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable, Iterator


MAX_SCANNED_BYTES = 5 * 1024 * 1024
PATH_REDACTION_KEY = os.urandom(32)
ABSOLUTE_USER_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])/(?:Users|home)/([^/\s\"'`<>\[\]{}$(),.;:]+)"
    r"(?=/|[\s\"'`<>\[\]{}$),.;:]|$)"
)
PUBLIC_HOME_SEGMENTS = frozenset(
    {"example", "username", "your-user", "your_user"}
)


def normalize_for_match(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def has_private_absolute_user_path(text: str) -> bool:
    return any(
        normalize_for_match(match.group(1)) not in PUBLIC_HOME_SEGMENTS
        for match in ABSOLUTE_USER_PATH_RE.finditer(text)
    )


def effective_private_markers(
    private_markers: Iterable[str], public_safe_terms: Iterable[str]
) -> tuple[str, ...]:
    safe_terms = {
        normalize_for_match(term.strip()) for term in public_safe_terms if term.strip()
    }
    return tuple(
        marker.strip()
        for marker in private_markers
        if marker.strip() and normalize_for_match(marker.strip()) not in safe_terms
    )


@dataclass(frozen=True, order=True)
class SecretFinding:
    rule_id: str
    path: str
    line: int
    scope: str = "worktree"

    def render(self) -> str:
        return f"{self.rule_id}\t{self.scope}\t{self.path}:{self.line}"


@dataclass(frozen=True)
class SecretScanResult:
    findings: tuple[SecretFinding, ...]

    @property
    def ok(self) -> bool:
        return not self.findings


@dataclass(frozen=True)
class Rule:
    rule_id: str
    pattern: re.Pattern[str]


RULES = (
    Rule(
        "PRIVATE_KEY",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    Rule(
        "GITHUB_TOKEN",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    ),
    Rule("AWS_ACCESS_KEY", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    Rule("SLACK_TOKEN", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    Rule("OPENAI_STYLE_TOKEN", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    Rule(
        "TELEGRAM_BOT_TOKEN",
        re.compile(r"\b\d{7,12}:[A-Za-z0-9_-]{30,}\b"),
    ),
    Rule(
        "BEARER_TOKEN",
        re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}", re.IGNORECASE),
    ),
    Rule("URL_CREDENTIAL", re.compile(r"://[^\s/:]+:[^\s/@]{8,}@")),
)

ASSIGNMENT = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password|passwd|secret|token)\b"
    r"\s*[:=]\s*[\"']?([^\s\"'`#,;)]{8,})"
)
PLACEHOLDER_VALUES = frozenset(
    (
        "example",
        "placeholder",
        "redacted",
        "changeme",
        "replace",
        "dummy",
        "xxx",
        "***",
    )
)
PLACEHOLDER_PREFIXES = (
    "example_",
    "example-",
    "placeholder_",
    "placeholder-",
    "redacted_",
    "redacted-",
    "replace_",
    "replace-",
    "dummy_",
    "dummy-",
    "your_",
    "your-",
)
PLACEHOLDER_WRAPPERS = (("${", "}"), ("{{", "}}"), ("<", ">"), ("[", "]"))
CREDENTIAL_REFERENCE_PATTERNS = (
    re.compile(r"^\$[A-Za-z_][A-Za-z0-9_]*$"),
    re.compile(r"^\{[A-Za-z_][A-Za-z0-9_]*\}$"),
    re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*\("),
    re.compile(
        r"^(?:os\.environ(?:\.get)?\(|os\.getenv\(|getenv\(|process\.env(?:\.|\[)|env(?:\.|\[))"
    ),
    re.compile(
        r"^(?=.*_)[A-Z][A-Z0-9_]*(?:API_KEY|ACCESS_TOKEN|AUTH_TOKEN|CLIENT_SECRET|PASSWORD|PASSWD|SECRET|TOKEN)$"
    ),
)

MarkerRule = tuple[str, str]


def _is_placeholder(raw_value: str) -> bool:
    folded = raw_value.casefold()
    return (
        folded in PLACEHOLDER_VALUES
        or folded.startswith(PLACEHOLDER_PREFIXES)
        or any(
            folded.startswith(opening) and folded.endswith(closing)
            for opening, closing in PLACEHOLDER_WRAPPERS
        )
    )


def _assignment_is_secret(line: str) -> bool:
    for match in ASSIGNMENT.finditer(line):
        raw_value = match.group(1)
        if _is_placeholder(raw_value):
            continue
        if any(pattern.search(raw_value) for pattern in CREDENTIAL_REFERENCE_PATTERNS):
            continue
        return True
    return False


def _compile_marker_rules(
    private_markers: Iterable[str], public_safe_terms: Iterable[str]
) -> tuple[MarkerRule, ...]:
    return tuple(
        (
            f"PRIVATE_MARKER_{hashlib.sha256(normalize_for_match(marker).encode('utf-8')).hexdigest()[:12]}",
            normalize_for_match(marker),
        )
        for marker in effective_private_markers(private_markers, public_safe_terms)
    )


def _scan_text(
    text: str,
    path: str,
    scope: str,
    marker_rules: tuple[MarkerRule, ...],
) -> tuple[SecretFinding, ...]:
    findings: set[SecretFinding] = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in RULES:
            if rule.pattern.search(line):
                findings.add(SecretFinding(rule.rule_id, path, line_number, scope))
        if _assignment_is_secret(line):
            findings.add(
                SecretFinding("GENERIC_CREDENTIAL_ASSIGNMENT", path, line_number, scope)
            )
        folded_line = normalize_for_match(line)
        if has_private_absolute_user_path(line):
            findings.add(SecretFinding("ABSOLUTE_USER_PATH", path, line_number, scope))
        for rule_id, marker in marker_rules:
            if marker in folded_line:
                findings.add(SecretFinding(rule_id, path, line_number, scope))
    return tuple(sorted(findings))


def scan_text(
    text: str,
    path: str,
    *,
    scope: str = "worktree",
    private_markers: Iterable[str] = (),
    public_safe_terms: Iterable[str] = (),
) -> tuple[SecretFinding, ...]:
    marker_rules = _compile_marker_rules(private_markers, public_safe_terms)
    return _scan_text(text, path, scope, marker_rules)


def _git(repository: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        input=input_bytes,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ValueError(f"Git command failed: {' '.join(args)}")
    return result.stdout


def _decode_text(content: bytes) -> str | None:
    if len(content) > MAX_SCANNED_BYTES or b"\0" in content:
        return None
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _read_bounded_file(path: Path) -> bytes:
    with path.open("rb") as handle:
        return handle.read(MAX_SCANNED_BYTES + 1)


def _read_git_payload(stream: BinaryIO, size: int) -> bytes | None:
    retained = bytearray() if size <= MAX_SCANNED_BYTES else None
    remaining = size
    while remaining:
        chunk = stream.read(min(64 * 1024, remaining))
        if not chunk:
            raise ValueError("Unexpected end of git cat-file output")
        if retained is not None:
            retained.extend(chunk)
        remaining -= len(chunk)
    return bytes(retained) if retained is not None else None


def _tracked_worktree_files(repository: Path) -> Iterator[tuple[str, bytes]]:
    for raw_path in _git(repository, "ls-files", "-z").split(b"\0"):
        if not raw_path:
            continue
        relative = raw_path.decode("utf-8", errors="surrogateescape")
        path = repository / relative
        if path.is_symlink():
            yield relative, os.readlink(path).encode("utf-8")
        elif path.is_file():
            yield relative, _read_bounded_file(path)


def _historical_text_objects(repository: Path) -> Iterator[tuple[str, str, bytes | None]]:
    object_paths: dict[str, set[str]] = {}
    for row in _git(repository, "rev-list", "--objects", "--all").decode(
        "utf-8", errors="replace"
    ).splitlines():
        parts = row.split(" ", 1)
        object_paths.setdefault(parts[0], set())
        if len(parts) == 2 and parts[1]:
            object_paths[parts[0]].add(parts[1])
    if not object_paths:
        return

    ordered_ids = tuple(sorted(object_paths))
    process = subprocess.Popen(
        ["git", "-C", str(repository), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    assert process.stderr is not None
    try:
        for requested_id in ordered_ids:
            process.stdin.write(f"{requested_id}\n".encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii", errors="replace").split()
            if len(header) != 3:
                raise ValueError("Invalid git cat-file header")
            object_id, object_type, raw_size = header
            size = int(raw_size)
            content = _read_git_payload(process.stdout, size)
            if process.stdout.read(1) != b"\n":
                raise ValueError("Unexpected end of git cat-file output")
            if object_type in {"commit", "tag"}:
                yield object_id, f"<git-{object_type}:{object_id[:12]}>", content
                continue
            if object_type != "blob":
                continue
            if not object_paths[requested_id]:
                yield object_id, f"<git-blob:{object_id[:12]}>", content
                continue
            for path in sorted(object_paths[requested_id]):
                yield object_id, path, content
    finally:
        process.stdin.close()
        return_code = process.wait()
        stderr = process.stderr.read()
        process.stdout.close()
        process.stderr.close()
        if return_code != 0:
            raise ValueError(
                f"Git command failed: cat-file --batch ({stderr.decode('utf-8', errors='replace').strip()})"
            )


def redact_path(path: str) -> str:
    return redact_value(path, "path")


def redact_value(value: str, label: str) -> str:
    token = hmac.new(
        PATH_REDACTION_KEY,
        value.encode("utf-8", errors="surrogateescape"),
        hashlib.sha256,
    ).hexdigest()[:12]
    return f"<redacted-{label}:{token}>"


def _scan_path(
    path: str,
    redacted_path: str,
    scope: str,
    marker_rules: tuple[MarkerRule, ...],
) -> tuple[SecretFinding, ...]:
    return _scan_text(path, redacted_path, scope, marker_rules)


def _unscannable_finding(redacted_path: str, scope: str) -> SecretFinding:
    return SecretFinding("UNSCANNABLE_CONTENT", redacted_path, 0, scope)


def scan_repository(
    repository: Path,
    *,
    include_history: bool,
    private_markers: Iterable[str] = (),
    public_safe_terms: Iterable[str] = (),
) -> SecretScanResult:
    root = repository.resolve()
    _git(root, "rev-parse", "--show-toplevel")
    marker_rules = _compile_marker_rules(private_markers, public_safe_terms)
    findings: set[SecretFinding] = set()
    for path, content in _tracked_worktree_files(root):
        redacted_path = redact_path(path)
        findings.update(_scan_path(path, redacted_path, "worktree-path", marker_rules))
        text = _decode_text(content)
        if text is None:
            findings.add(_unscannable_finding(redacted_path, "worktree"))
            continue
        findings.update(
            _scan_text(
                text,
                redacted_path,
                "worktree",
                marker_rules,
            )
        )
    if include_history:
        for object_id, path, content in _historical_text_objects(root):
            redacted_path = redact_path(path)
            findings.update(
                _scan_path(
                    path,
                    redacted_path,
                    f"history-path:{object_id[:12]}",
                    marker_rules,
                )
            )
            if content is None:
                findings.add(
                    _unscannable_finding(redacted_path, f"history:{object_id[:12]}")
                )
                continue
            text = _decode_text(content)
            if text is None:
                findings.add(
                    _unscannable_finding(redacted_path, f"history:{object_id[:12]}")
                )
                continue
            findings.update(
                _scan_text(
                    text,
                    redacted_path,
                    f"history:{object_id[:12]}",
                    marker_rules,
                )
            )
    return SecretScanResult(tuple(sorted(findings)))
