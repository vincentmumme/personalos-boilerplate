from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath

from .catalog import ModuleCatalogError, load_module_catalog
from .inventory import git_tracked_files
from .secrets import effective_private_markers, redact_path, redact_value
from .sync import BUILD_CONTRACT, WIKILINK_RE, _privacy_findings


@dataclass(frozen=True)
class AuditFinding:
    code: str
    path: str
    detail: str


@dataclass(frozen=True)
class AuditResult:
    findings: tuple[AuditFinding, ...]

    @property
    def ok(self) -> bool:
        return not self.findings


FENCED_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)


def _is_placeholder_link(target: str) -> bool:
    return (
        "{{" in target
        or "<" in target
        or "..." in target
        or "YYYY" in target
        or target in {"slug", "voller/vault-relativer/pfad", "path/to/source"}
        or target.startswith("path/to/")
    )


def _virtual_files(build_root: Path) -> tuple[dict[str, Path], list[AuditFinding]]:
    files: dict[str, Path] = {}
    findings: list[AuditFinding] = []
    template = build_root / "core"
    if template.is_dir():
        for path in sorted(item for item in template.rglob("*") if item.is_file()):
            files[path.relative_to(template).as_posix()] = path
    modules = build_root / "modules"
    if modules.is_dir():
        for module in sorted(path for path in modules.iterdir() if path.is_dir()):
            payload = module / "payload"
            if not payload.is_dir():
                continue
            for path in sorted(item for item in payload.rglob("*") if item.is_file()):
                relative = path.relative_to(payload).as_posix()
                if relative in files:
                    findings.append(
                        AuditFinding(
                            "module-path-collision",
                            relative,
                            f"Module {module.name} collides with another logical file",
                        )
                    )
                    continue
                files[relative] = path
    return files, findings


def _resolves(target: str, source_path: str, logical_files: dict[str, Path]) -> bool:
    normalized = target.strip().lstrip("/")
    candidates = [normalized]
    if not PurePosixPath(normalized).suffix:
        candidates.extend([f"{normalized}.md", f"{normalized}/index.md"])
    parent = PurePosixPath(source_path).parent
    if parent != PurePosixPath("."):
        candidates.extend((parent / candidate).as_posix() for candidate in list(candidates))
    if any(candidate in logical_files for candidate in candidates):
        return True
    if "/" not in normalized:
        stem = PurePosixPath(normalized).stem
        return sum(PurePosixPath(path).stem == stem for path in logical_files) == 1
    return False


def audit_build(
    build_root: Path,
    private_markers: list[str],
    public_safe_terms: tuple[str, ...] = (),
) -> AuditResult:
    findings: list[AuditFinding] = []
    private_markers = list(effective_private_markers(private_markers, public_safe_terms))
    manifest_path = build_root / "manifest.json"
    if not manifest_path.is_file():
        return AuditResult((AuditFinding("missing-manifest", "manifest.json", "Build manifest is missing"),))
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return AuditResult((AuditFinding("invalid-manifest", "manifest.json", str(exc)),))
    if manifest.get("schema_version") != 2 or manifest.get("build_contract") != BUILD_CONTRACT:
        findings.append(
            AuditFinding(
                "invalid-build-contract",
                "manifest.json",
                "Manifest does not identify an owned PersonalOS Boilerplate build",
            )
        )
    required_metadata = {
        "boilerplate_version": str,
        "source_revision": str,
        "source_date": str,
        "counts": dict,
    }
    for field, expected_type in required_metadata.items():
        if not isinstance(manifest.get(field), expected_type) or not manifest.get(field):
            findings.append(
                AuditFinding("invalid-manifest", "manifest.json", f"Missing or invalid {field}")
            )
    if isinstance(manifest.get("boilerplate_version"), str) and not re.fullmatch(
        r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)",
        manifest["boilerplate_version"],
    ):
        findings.append(AuditFinding("invalid-manifest", "manifest.json", "Invalid version"))
    if isinstance(manifest.get("source_revision"), str) and not re.fullmatch(
        r"[0-9a-f]{40}", manifest["source_revision"]
    ):
        findings.append(AuditFinding("invalid-manifest", "manifest.json", "Invalid source revision"))
    if isinstance(manifest.get("source_date"), str):
        try:
            datetime.fromisoformat(manifest["source_date"])
        except ValueError:
            findings.append(AuditFinding("invalid-manifest", "manifest.json", "Invalid source date"))
    counts = manifest.get("counts")
    if isinstance(counts, dict) and not all(
        isinstance(key, str) and isinstance(value, int) and value >= 0
        for key, value in counts.items()
    ):
        findings.append(AuditFinding("invalid-manifest", "manifest.json", "Invalid counts"))
    for marker in _privacy_findings(manifest_path.read_bytes(), private_markers):
        findings.append(AuditFinding("privacy-marker", redact_path("manifest.json"), marker))

    declared: set[str] = set()
    raw_managed = manifest.get("managed_files", [])
    if not isinstance(raw_managed, list):
        raw_managed = []
        findings.append(
            AuditFinding("invalid-manifest", "manifest.json", "managed_files must be a list")
        )
    for item in raw_managed:
        if not isinstance(item, dict):
            findings.append(AuditFinding("invalid-manifest-entry", "manifest.json", "Expected object"))
            continue
        if not all(
            isinstance(item.get(field), str) and item.get(field)
            for field in ("sha256", "source_path", "rule_id")
        ) or not re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256", ""))):
            findings.append(
                AuditFinding("invalid-manifest-entry", "manifest.json", "Incomplete managed entry")
            )
            continue
        relative = item.get("path", "")
        if not isinstance(relative, str):
            findings.append(AuditFinding("unsafe-manifest-path", str(relative), "Unsafe path"))
            continue
        pure = PurePosixPath(relative)
        if (
            not relative
            or relative in {".", ".."}
            or "\\" in relative
            or pure.is_absolute()
            or ".." in pure.parts
        ):
            findings.append(AuditFinding("unsafe-manifest-path", str(relative), "Unsafe path"))
            continue
        if relative in declared:
            findings.append(AuditFinding("duplicate-manifest-path", relative, "Path is repeated"))
            continue
        declared.add(relative)
        path = build_root / relative
        if (
            not path.resolve().is_relative_to(build_root.resolve())
            or path.is_symlink()
            or not path.is_file()
        ):
            findings.append(AuditFinding("manifest-file-missing", relative, "Declared file is missing"))
            continue
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if digest != item.get("sha256"):
            findings.append(
                AuditFinding("manifest-hash-mismatch", relative, "File differs from its build manifest")
            )
        for marker in _privacy_findings(relative.encode("utf-8") + b"\n" + content, private_markers):
            findings.append(AuditFinding("privacy-marker", redact_path(relative), marker))
    actual: set[str] = set()
    template_root = build_root / "core"
    if template_root.is_dir():
        actual.update(
            path.relative_to(build_root).as_posix()
            for path in template_root.rglob("*")
            if path.is_file()
        )
    modules_root = build_root / "modules"
    if modules_root.is_dir():
        catalog_path = modules_root / "catalog.json"
        if catalog_path.is_file():
            actual.add(catalog_path.relative_to(build_root).as_posix())
        for payload in modules_root.glob("*/payload"):
            actual.update(
                path.relative_to(build_root).as_posix()
                for path in payload.rglob("*")
                if path.is_file()
            )
    reference_root = build_root / "reference"
    if reference_root.is_dir():
        actual.update(
            path.relative_to(build_root).as_posix()
            for path in reference_root.rglob("*")
            if path.is_file()
        )
    for relative in sorted(actual - declared):
        findings.append(AuditFinding("unmanaged-build-file", relative, "File is absent from manifest"))

    try:
        load_module_catalog(build_root)
    except ModuleCatalogError as exc:
        findings.append(AuditFinding("invalid-module-catalog", "modules/catalog.json", str(exc)))

    if (build_root / ".git").exists():
        for relative in git_tracked_files(build_root):
            if relative == "manifest.json" or relative in declared:
                continue
            path = build_root / relative
            if not path.is_file() or path.is_symlink():
                continue
            for marker in _privacy_findings(
                relative.encode("utf-8") + b"\n" + path.read_bytes(), private_markers
            ):
                findings.append(AuditFinding("privacy-marker", redact_path(relative), marker))

    logical_files, overlay_findings = _virtual_files(build_root)
    findings.extend(overlay_findings)
    reference_files = {
        path.relative_to(reference_root).as_posix(): path
        for path in reference_root.rglob("*")
        if path.is_file()
    } if reference_root.is_dir() else {}
    if set(reference_files) != set(logical_files):
        for relative in sorted(set(logical_files) - set(reference_files)):
            findings.append(AuditFinding("reference-file-missing", relative, "Missing from reference"))
        for relative in sorted(set(reference_files) - set(logical_files)):
            findings.append(AuditFinding("reference-file-extra", relative, "Not produced by core or modules"))
    for relative in sorted(set(reference_files) & set(logical_files)):
        if reference_files[relative].read_bytes() != logical_files[relative].read_bytes():
            findings.append(AuditFinding("reference-content-mismatch", relative, "Reference differs from composition"))
    for relative, path in sorted(logical_files.items()):
        content = path.read_bytes()
        if path.suffix.lower() != ".md":
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        visible_text = FENCED_BLOCK_RE.sub("", text)
        for match in WIKILINK_RE.finditer(visible_text):
            target = match.group(1).strip()
            if _is_placeholder_link(target):
                continue
            if not _resolves(target, relative, logical_files):
                findings.append(
                    AuditFinding(
                        "broken-wikilink",
                        relative,
                        target,
                    )
                )
    if private_markers:
        findings = [
            AuditFinding(
                item.code,
                redact_path(item.path),
                redact_value(item.detail, "detail"),
            )
            for item in findings
        ]
    return AuditResult(tuple(sorted(findings, key=lambda item: (item.code, item.path, item.detail))))
