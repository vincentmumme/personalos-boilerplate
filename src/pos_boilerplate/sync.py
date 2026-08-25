from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .catalog import ModuleCatalogError, load_module_catalog
from .inventory import git_committed_files, inventory
from .policy import Classification, ExportPolicy
from .secrets import effective_private_markers, has_private_absolute_user_path, normalize_for_match


class SyncError(RuntimeError):
    """Raised when a deterministic boilerplate build cannot complete."""


class PrivacyError(SyncError):
    """Raised when private markers survive the public derivation."""


class UnsafeOutputError(SyncError):
    """Raised before sync could replace a directory it does not own."""


BUILD_CONTRACT = "personalos-boilerplate-build/v2"
BOILERPLATE_VERSION = "0.1.0"


@dataclass(frozen=True)
class SyncConfig:
    source: Path
    output: Path
    policy: ExportPolicy
    replacements: dict[str, str]
    private_markers: list[str]
    blueprints: Path | None = None
    public_safe_terms: tuple[str, ...] = ()


@dataclass(frozen=True)
class SyncResult:
    source_revision: str
    managed_files: tuple[str, ...]
    counts: dict[str, int]


def _git(source: Path, *args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(source), *args],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SyncError(f"Git source read failed for {' '.join(args)}: {exc}") from exc
    return result.stdout


def _source_revision(source: Path) -> str:
    return _git(source, "rev-parse", "HEAD").decode("ascii").strip()


def _source_date(source: Path, revision: str) -> str:
    return _git(source, "show", "-s", "--format=%cI", revision).decode("utf-8").strip()


def _validate_output_target(source: Path, output: Path) -> None:
    source_resolved = source.resolve()
    output_resolved = output.resolve()
    if (
        source_resolved == output_resolved
        or source_resolved.is_relative_to(output_resolved)
        or output_resolved.is_relative_to(source_resolved)
    ):
        raise UnsafeOutputError(
            f"Sync output and private source repository may not overlap: {output_resolved}"
        )
    if output.is_symlink():
        raise UnsafeOutputError(f"Sync output may not be a symlink: {output}")
    if not output.exists():
        return
    if not output.is_dir():
        raise UnsafeOutputError(f"Sync output exists but is not a directory: {output}")
    if (output / ".git").exists():
        raise UnsafeOutputError(f"Refusing to replace a Git repository: {output_resolved}")
    if not (output / "manifest.json").is_file():
        raise UnsafeOutputError(
            f"Refusing to replace an unmanaged directory without manifest.json: {output_resolved}"
        )
    _validate_owned_output(output)


def _safe_build_path(root: Path, relative: str) -> Path:
    if not relative or relative in {".", ".."} or "\\" in relative:
        raise UnsafeOutputError(f"Unsafe build path: {relative!r}")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise UnsafeOutputError(f"Unsafe build path: {relative!r}")
    candidate = root.joinpath(*pure.parts)
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise UnsafeOutputError(f"Build path escapes output root: {relative!r}")
    return candidate


def _validate_owned_output(output: Path) -> None:
    """Prove that an existing directory is exactly one build we generated."""

    manifest_path = output / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UnsafeOutputError(f"Existing build manifest is invalid: {output}") from exc
    if manifest.get("schema_version") != 2 or manifest.get("build_contract") != BUILD_CONTRACT:
        raise UnsafeOutputError(f"Existing directory is not an owned boilerplate build: {output}")
    raw_managed = manifest.get("managed_files")
    if not isinstance(raw_managed, list):
        raise UnsafeOutputError(f"Existing build manifest has no managed file list: {output}")
    declared: set[str] = set()
    for item in raw_managed:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise UnsafeOutputError(f"Existing build manifest contains an invalid entry: {output}")
        relative = item["path"]
        if relative in declared:
            raise UnsafeOutputError(f"Existing build manifest contains duplicate paths: {relative}")
        declared.add(relative)
        path = _safe_build_path(output, relative)
        if path.is_symlink() or not path.is_file():
            raise UnsafeOutputError(f"Existing managed file is missing or unsafe: {relative}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item.get("sha256"):
            raise UnsafeOutputError(f"Existing managed file differs from manifest: {relative}")
    actual = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual != declared | {"manifest.json"}:
        raise UnsafeOutputError(f"Existing build contains unmanaged or missing files: {output}")


def _publish_staging(staging: Path, output: Path) -> None:
    if not output.exists():
        os.replace(staging, output)
        return
    backup = Path(tempfile.mkdtemp(prefix=f".{output.name}-backup-", dir=output.parent))
    backup.rmdir()
    os.replace(output, backup)
    try:
        _validate_owned_output(backup)
        os.replace(staging, output)
    except Exception:
        if not output.exists():
            os.replace(backup, output)
        raise
    shutil.rmtree(backup)


def _source_blobs(source: Path, revision: str, relative_paths: list[str]) -> dict[str, bytes]:
    if not relative_paths:
        return {}
    try:
        process = subprocess.Popen(
            ["git", "-C", str(source), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise SyncError(f"Could not start Git batch reader: {exc}") from exc
    if process.stdin is None or process.stdout is None:
        process.kill()
        raise SyncError("Git batch reader did not expose pipes")

    blobs: dict[str, bytes] = {}
    try:
        for relative_path in relative_paths:
            if "\n" in relative_path or "\r" in relative_path:
                raise SyncError(f"Git batch reader does not support newline paths: {relative_path!r}")
            process.stdin.write(f"{revision}:{relative_path}\n".encode("utf-8"))
            process.stdin.flush()
            header = process.stdout.readline().decode("utf-8", errors="replace").strip()
            parts = header.rsplit(" ", 2)
            if len(parts) != 3 or not parts[2].isdigit():
                raise SyncError(f"Git object read failed for {relative_path}: {header}")
            size = int(parts[2])
            content = process.stdout.read(size)
            delimiter = process.stdout.read(1)
            if len(content) != size or delimiter != b"\n":
                raise SyncError(f"Incomplete Git object read for {relative_path}")
            blobs[relative_path] = content
        process.stdin.close()
        return_code = process.wait()
        if return_code != 0:
            stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
            raise SyncError(f"Git batch reader failed: {stderr.strip()}")
        return blobs
    except Exception:
        process.kill()
        process.wait()
        raise
    finally:
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None and not stream.closed:
                stream.close()


def _apply_replacements(content: str, replacements: dict[str, str]) -> str:
    for old, new in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        content = content.replace(old, new)
    return content


WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(?:\|([^\]]+))?\]\]")
DECISION_REFS_RE = re.compile(
    r"(?m)^(?P<indent>[ \t]*)decision_refs:[ \t]*\[(?P<refs>[^\n]*)\][ \t]*$"
)
PUBLIC_ADOPTION_DECISION = (
    "[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"
)
VALIDATOR_TEST_RE = re.compile(
    r"(?m)^(?P<indent>[ \t]*)validator_test:[ \t]*[\"']?system/data-model/tests/[^\n\"']+[\"']?[ \t]*$"
)
CODE_PATH_RE = re.compile(r"`([^`\n]+)`")
MARKDOWN_LINK_PATH_RE = re.compile(r"\]\(([^)]+)\)")
PORTABILITY_REWRITES = {
    "system/runbooks/agents/scripts/relink-skills.sh":
        "system/checks/system/scripts/check-resolvable.py",
}


def _normalize_private_decision_provenance(content: str) -> str:
    """Point exported norms at the installer's public adoption decision.

    Private PersonalOS decisions are instance history and cannot ship. Exported
    system records still require honest local provenance, so installation creates
    one explicit decision that adopts the public foundation.
    """

    def replace(match: re.Match[str]) -> str:
        refs = match.group("refs")
        if "[[decisions/" not in refs:
            return match.group(0)
        return (
            f'{match.group("indent")}decision_refs: '
            f'["{PUBLIC_ADOPTION_DECISION}"]'
        )

    return DECISION_REFS_RE.sub(replace, content)


def _normalize_validator_test_paths(content: str) -> str:
    return VALIDATOR_TEST_RE.sub(
        lambda match: (
            f'{match.group("indent")}validator_test: '
            "system/data-model/tests/test_registry_contract.py"
        ),
        content,
    )


def _normalize_change_history(content: str) -> str:
    marker = "## Change History\n"
    index = content.rfind(marker)
    if index < 0:
        return content
    return (
        content[:index]
        + marker
        + "\n- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.\n"
    )


def _remove_excluded_wikilinks(
    content: str,
    source_path: str,
    source_paths: set[str],
    source_stems: dict[str, list[str]],
    classifications: dict[str, Classification],
) -> str:
    def replace(match: re.Match[str], field: str | None) -> str:
        target = match.group(1).strip()
        if "{{" in target or "<" in target or "://" in target:
            return match.group(0)
        candidate = target if Path(target).suffix else f"{target}.md"
        candidates = [candidate]
        source_parent = PurePosixPath(source_path).parent
        if source_parent != PurePosixPath("."):
            candidates.append((source_parent / candidate).as_posix())
        if "/" not in target:
            candidates.extend(source_stems.get(Path(target).stem, []))
        classification = None
        for possible_path in candidates:
            if possible_path not in source_paths:
                continue
            classification = classifications.get(possible_path)
            if classification is not None:
                break
        if classification is None:
            return match.group(0)
        if classification.action != "exclude":
            return match.group(0)
        if field:
            neutral_targets = {
                "decision_refs": PUBLIC_ADOPTION_DECISION,
                "evidence_refs": PUBLIC_ADOPTION_DECISION,
                "affected_owner_refs": "[[system/index]]",
                "decided_by_refs": "[[USER]]",
                "participant_refs": "[[USER]]",
                "subject_ref": "[[identity/me]]",
                "system_refs": "[[system/contracts/normative-system-architecture]]",
                "verifies_refs": "[[system/contracts/normative-system-architecture]]",
                "derived_from_refs": "[[system/contracts/normative-system-architecture]]",
                "supersedes_refs": "[[system/contracts/normative-system-architecture]]",
                "producer_skill_ref": "[[skills/pos-verify/SKILL]]",
                "invokes_skill_refs": "[[skills/pos-verify/SKILL]]",
                "owning_skill_ref": "[[skills/pos-verify/SKILL]]",
            }
            if field in neutral_targets:
                return neutral_targets[field]
            if field.endswith("_ref") or field.endswith("_refs"):
                # Profiles and fixtures require relation-shaped placeholders. These
                # example refs are schema samples, not installed instance records.
                slug = field.removesuffix("_refs").removesuffix("_ref").replace("_", "-")
                return f"[[examples/{slug}]]"
        alias = match.group(3)
        return alias.strip() if alias else Path(target).name.replace("-", " ")

    rendered_lines: list[str] = []
    for line in content.splitlines(keepends=True):
        field_match = re.match(r"^[ \t]*([a-z][a-z0-9_]*):", line)
        field = field_match.group(1) if field_match else None
        rendered_lines.append(WIKILINK_RE.sub(lambda match: replace(match, field), line))
    return "".join(rendered_lines)


def _remove_excluded_resource_lines(
    content: str,
    source_path: str,
    source_paths: set[str],
    classifications: dict[str, Classification],
) -> str:
    """Drop instructions that point only at resources absent from the public build."""

    source_parent = PurePosixPath(source_path).parent
    rendered_lines: list[str] = []
    for line in content.splitlines(keepends=True):
        referenced_paths = []
        tokens = CODE_PATH_RE.findall(line) + MARKDOWN_LINK_PATH_RE.findall(line)
        for token in tokens:
            if "://" in token or token.startswith("--") or " " in token:
                continue
            candidate = (source_parent / token).as_posix()
            if candidate in source_paths:
                referenced_paths.append(candidate)
        if referenced_paths and all(
            classifications[path].action == "exclude" for path in referenced_paths
        ):
            continue
        rendered_lines.append(line)
    return "".join(rendered_lines)


def _target_for(classification: Classification) -> str | None:
    if classification.action == "exclude":
        return None
    if classification.target:
        return PurePosixPath(classification.target).as_posix()
    if classification.action in {"copy", "render"}:
        return f"core/{classification.path}"
    if classification.action == "module":
        if not classification.module:
            raise SyncError(f"Module classification has no module: {classification.path}")
        return f"modules/{classification.module}/payload/{classification.path}"
    if classification.action == "fixture":
        return f"examples/fixtures/{classification.path}"
    raise SyncError(f"Unsupported sync action: {classification.action}")


def _blueprint_bytes(config: SyncConfig, target: str) -> bytes | None:
    if config.blueprints is None:
        return None
    if target.startswith("core/"):
        relative = target.removeprefix("core/")
    elif target.startswith("modules/") and "/payload/" in target:
        relative = target.split("/payload/", 1)[1]
    else:
        return None
    candidate = config.blueprints / relative
    if not candidate.is_file():
        return None
    if candidate.is_symlink() or not candidate.resolve().is_relative_to(config.blueprints.resolve()):
        raise SyncError(f"Blueprint path is unsafe: {candidate}")
    return candidate.read_bytes()


def _render_bytes(
    config: SyncConfig,
    classification: Classification,
    target: str,
    source_paths: set[str],
    source_stems: dict[str, list[str]],
    classifications: dict[str, Classification],
    source_blobs: dict[str, bytes],
) -> bytes:
    blueprint = (
        _blueprint_bytes(config, target)
        if classification.action in {"render", "module"}
        else None
    )
    raw = blueprint if blueprint is not None else source_blobs[classification.path]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        if classification.action in {"render", "fixture"}:
            raise SyncError(f"Cannot render non-text source: {classification.path}")
        return raw
    if classification.action in {"render", "module", "fixture"}:
        if blueprint is None:
            text = _normalize_private_decision_provenance(text)
            text = _normalize_validator_test_paths(text)
            text = _normalize_change_history(text)
            text = _remove_excluded_wikilinks(
                text,
                classification.path,
                source_paths,
                source_stems,
                classifications,
            )
            text = _remove_excluded_resource_lines(
                text,
                classification.path,
                source_paths,
                classifications,
            )
        text = _apply_replacements(text, PORTABILITY_REWRITES)
        text = _apply_replacements(text, config.replacements)
        text = text.rstrip() + "\n"
    return text.encode("utf-8")


def _privacy_findings(content: bytes, markers: list[str]) -> list[str]:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return ["binary-content-unscannable"]
    folded = normalize_for_match(text)
    findings = [
        f"private-marker:{hashlib.sha256(normalize_for_match(marker).encode('utf-8')).hexdigest()[:12]}"
        for marker in markers
        if marker and normalize_for_match(marker) in folded
    ]
    if has_private_absolute_user_path(text):
        findings.append("absolute-user-path")
    return sorted(set(findings))


def _add_blueprint_tree(
    *,
    root: Path,
    blueprints_root: Path,
    staging: Path,
    target_prefix: str,
    source_prefix: str,
    rule_id: str,
    private_markers: list[str],
    managed: list[dict[str, str]],
    existing_targets: set[str],
    findings: dict[str, list[str]],
) -> None:
    if root.is_symlink():
        raise SyncError(f"Blueprint subtree may not be a symlink: {root}")
    if not root.is_dir():
        return
    resolved_blueprints = blueprints_root.resolve()
    resolved_root = root.resolve()
    if not resolved_root.is_relative_to(resolved_blueprints):
        raise SyncError(f"Blueprint subtree escapes its root: {root}")
    for blueprint_path in sorted(path for path in root.rglob("*") if path.is_file()):
        if blueprint_path.is_symlink() or not blueprint_path.resolve().is_relative_to(
            resolved_root
        ) or not blueprint_path.resolve().is_relative_to(
            resolved_blueprints
        ):
            raise SyncError(f"Blueprint path is unsafe: {blueprint_path}")
        relative = blueprint_path.relative_to(root).as_posix()
        target = f"{target_prefix}/{relative}"
        if target in existing_targets:
            raise SyncError(f"Blueprint collides with generated target: {target}")
        existing_targets.add(target)
        content = blueprint_path.read_bytes()
        try:
            content = (content.decode("utf-8").rstrip() + "\n").encode("utf-8")
        except UnicodeDecodeError:
            pass
        private = _privacy_findings(
            target.encode("utf-8") + b"\n" + content,
            private_markers,
        )
        if private:
            findings[target] = private
            continue
        destination = staging / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        managed.append(
            {
                "path": target,
                "sha256": hashlib.sha256(content).hexdigest(),
                "source_path": f"blueprint:{source_prefix}/{relative}",
                "rule_id": rule_id,
            }
        )


def sync_repository(config: SyncConfig) -> SyncResult:
    _validate_output_target(config.source, config.output)
    revision = _source_revision(config.source)
    source_date = _source_date(config.source, revision)
    private_markers = list(
        effective_private_markers(config.private_markers, config.public_safe_terms)
    )
    source_paths = git_committed_files(config.source, revision)
    source_path_set = set(source_paths)
    source_stems: dict[str, list[str]] = {}
    for source_path in source_paths:
        source_stems.setdefault(Path(source_path).stem, []).append(source_path)
    source_inventory = inventory(source_paths, config.policy)
    if source_inventory.unclassified:
        raise SyncError(
            f"Cannot sync with {len(source_inventory.unclassified)} unclassified source files"
        )
    classifications = {item.path: item for item in source_inventory.files}
    source_blobs = _source_blobs(
        config.source,
        revision,
        [item.path for item in source_inventory.files if item.action != "exclude"],
    )

    output_parent = config.output.parent
    output_parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{config.output.name}-", dir=output_parent))
    managed: list[dict[str, str]] = []
    existing_targets: set[str] = set()
    findings: dict[str, list[str]] = {}
    try:
        for classification in source_inventory.files:
            target = _target_for(classification)
            if target is None:
                continue
            _safe_build_path(staging, target)
            if target in existing_targets:
                raise SyncError(f"Several policy rules produce the same target: {target}")
            existing_targets.add(target)
            content = _render_bytes(
                config,
                classification,
                target,
                source_path_set,
                source_stems,
                classifications,
                source_blobs,
            )
            private = _privacy_findings(
                target.encode("utf-8") + b"\n" + content,
                private_markers,
            )
            if private:
                findings[target] = private
                continue
            destination = staging / target
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            managed.append(
                {
                    "path": target,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "source_path": classification.path,
                    "rule_id": classification.rule_id,
                }
            )
        if config.blueprints is not None:
            _add_blueprint_tree(
                root=config.blueprints / "_static",
                blueprints_root=config.blueprints,
                staging=staging,
                target_prefix="core",
                source_prefix="_static",
                rule_id="static-blueprint",
                private_markers=private_markers,
                managed=managed,
                existing_targets=existing_targets,
                findings=findings,
            )
            _add_blueprint_tree(
                root=config.blueprints / "_modules",
                blueprints_root=config.blueprints,
                staging=staging,
                target_prefix="modules",
                source_prefix="_modules",
                rule_id="module-blueprint",
                private_markers=private_markers,
                managed=managed,
                existing_targets=existing_targets,
                findings=findings,
            )
        if findings:
            examples = "; ".join(
                f"{path}: {', '.join(markers)}"
                for path, markers in list(sorted(findings.items()))[:10]
            )
            raise PrivacyError(
                f"Private markers survived in {len(findings)} generated files. {examples}"
            )

        catalog_path = staging / "modules/catalog.json"
        if not catalog_path.is_file():
            module_ids = sorted(
                path.name
                for path in (staging / "modules").iterdir()
                if path.is_dir() and (path / "payload").is_dir()
            ) if (staging / "modules").is_dir() else []
            catalog = {
                "schema_version": 1,
                "default_enabled": [],
                "modules": [
                    {
                        "id": module_id,
                        "kind": "extension",
                        "title": module_id,
                        "entry": module_id,
                    }
                    for module_id in module_ids
                ],
            }
            content = (json.dumps(catalog, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            catalog_path.parent.mkdir(parents=True, exist_ok=True)
            catalog_path.write_bytes(content)
            existing_targets.add("modules/catalog.json")
            managed.append(
                {
                    "path": "modules/catalog.json",
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "source_path": "generated:module-catalog",
                    "rule_id": "module-catalog",
                }
            )
        try:
            load_module_catalog(staging)
        except ModuleCatalogError as exc:
            raise SyncError(str(exc)) from exc

        # The complete reference is never edited independently. It is the exact
        # overlay of the mandatory core and every optional module payload.
        reference_sources: dict[str, tuple[Path, str]] = {}
        core_root = staging / "core"
        for path in sorted(item for item in core_root.rglob("*") if item.is_file()):
            reference_sources[path.relative_to(core_root).as_posix()] = (path, "core")
        modules_root = staging / "modules"
        if modules_root.is_dir():
            for payload in sorted(modules_root.glob("*/payload")):
                for path in sorted(item for item in payload.rglob("*") if item.is_file()):
                    relative = path.relative_to(payload).as_posix()
                    if relative in reference_sources:
                        owner = reference_sources[relative][1]
                        raise SyncError(
                            f"Module {payload.parent.name} collides with {owner}: {relative}"
                        )
                    reference_sources[relative] = (path, f"module:{payload.parent.name}")
        for relative, (source_path, owner) in sorted(reference_sources.items()):
            target = f"reference/{relative}"
            content = source_path.read_bytes()
            destination = staging / target
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            managed.append(
                {
                    "path": target,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "source_path": f"generated:{owner}/{relative}",
                    "rule_id": "reference-composition",
                }
            )

        counts = dict(sorted(Counter(item.action for item in source_inventory.files).items()))
        manifest = {
            "schema_version": 2,
            "build_contract": BUILD_CONTRACT,
            "boilerplate_version": BOILERPLATE_VERSION,
            "source_revision": revision,
            "source_date": source_date,
            "counts": counts,
            "managed_files": sorted(managed, key=lambda item: item["path"]),
        }
        manifest_bytes = (
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")
        manifest_findings = _privacy_findings(manifest_bytes, private_markers)
        if manifest_findings:
            raise PrivacyError(
                "Private markers survived in generated manifest metadata: "
                + ", ".join(manifest_findings)
            )
        (staging / "manifest.json").write_bytes(manifest_bytes)
        _validate_output_target(config.source, config.output)
        _publish_staging(staging, config.output)
        return SyncResult(
            source_revision=revision,
            managed_files=tuple(item["path"] for item in manifest["managed_files"]),
            counts=counts,
        )
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
