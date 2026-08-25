from __future__ import annotations

import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .audit import audit_build
from .catalog import ModuleSpec, load_module_catalog


class InstallError(RuntimeError):
    """Raised when a clean PersonalOS installation cannot be completed safely."""


@dataclass(frozen=True)
class InstallConfig:
    build_root: Path
    destination: Path
    modules: tuple[str, ...] | None
    values: dict[str, str]
    rebuild_data_model: bool = True


@dataclass(frozen=True)
class InstallResult:
    destination: Path
    modules: tuple[str, ...]
    file_count: int


PLACEHOLDER_RE = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")
EXECUTABLE_TEXT_SUFFIXES = frozenset(
    {".bash", ".cjs", ".fish", ".js", ".mjs", ".php", ".pl", ".ps1", ".py", ".rb", ".sh", ".ts", ".zsh"}
)
HUMAN_VALUE_FIELDS = frozenset(
    {"user_name", "user_last_name", "organization_name", "example_person_name"}
)
SAFE_HUMAN_VALUE_RE = re.compile(r"[\w .&'()/+\-]+", re.UNICODE)
SLUG_VALUE_FIELDS = frozenset({"user_slug", "organization_slug"})
SAFE_SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def _uuid() -> str:
    factory = getattr(uuid, "uuid7", None)
    if factory is not None:
        return str(factory())

    timestamp_ms = time.time_ns() // 1_000_000
    random_bits = secrets.randbits(74)
    value = (timestamp_ms & ((1 << 48) - 1)) << 80
    value |= 0x7 << 76
    value |= ((random_bits >> 62) & 0xFFF) << 64
    value |= 0b10 << 62
    value |= random_bits & ((1 << 62) - 1)
    return str(uuid.UUID(int=value))


def _default_values(destination: Path) -> dict[str, str]:
    install_date = date.today().isoformat()
    return {
        "install_date": install_date,
        "install_year": install_date[:4],
        "personalos_root": str(destination),
        "workspace_root": str(destination.parent),
        "home_dir": str(Path.home()),
        "service_home": str(Path.home()),
        "organization_name": "Keine Organisation hinterlegt",
        "organization_slug": "keine-organisation",
        "example_person_name": "Alex Example",
    }


def _is_install_placeholder(name: str) -> bool:
    return (
        name.startswith("id_")
        or name.startswith("user_")
        or name.startswith("organization_")
        or name.startswith("installed_modules_")
        or name
        in {
            "install_date",
            "install_year",
            "personalos_root",
            "workspace_root",
            "home_dir",
            "service_home",
            "example_person_name",
        }
    )


def _render_text(text: str, values: dict[str, str], ids: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name.startswith("id_"):
            return ids.setdefault(name, _uuid())
        if name in values:
            return values[name]
        return match.group(0)

    rendered = PLACEHOLDER_RE.sub(replace, text)
    unresolved = sorted(
        {
            match.group(1)
            for match in PLACEHOLDER_RE.finditer(rendered)
            if _is_install_placeholder(match.group(1))
        }
    )
    if unresolved:
        raise InstallError(f"Missing install values: {', '.join(unresolved)}")
    return rendered


def _assert_safe_executable_template(relative: str, text: str) -> None:
    if (
        Path(relative).suffix.casefold() not in EXECUTABLE_TEXT_SUFFIXES
        and not text.startswith("#!")
    ):
        return
    placeholders = sorted(
        {
            match.group(1)
            for match in PLACEHOLDER_RE.finditer(text)
            if _is_install_placeholder(match.group(1))
        }
    )
    if placeholders:
        raise InstallError(
            "Install values are not allowed in executable template "
            f"{relative}: {', '.join(placeholders)}"
        )


def _validate_human_values(values: dict[str, str]) -> None:
    for field in HUMAN_VALUE_FIELDS:
        value = values.get(field)
        if value and not SAFE_HUMAN_VALUE_RE.fullmatch(value):
            raise InstallError(f"Unsafe characters in {field}")


def _validate_slug_values(values: dict[str, str]) -> None:
    for field in SLUG_VALUE_FIELDS:
        value = values.get(field)
        if value and not SAFE_SLUG_RE.fullmatch(value):
            raise InstallError(f"Invalid slug in {field}")


def _render_relative_path(relative: str, values: dict[str, str], ids: dict[str, str]) -> str:
    rendered = _render_text(relative, values, ids)
    candidate = Path(rendered)
    if candidate.is_absolute() or ".." in candidate.parts or rendered in {"", "."}:
        raise InstallError(f"Unsafe rendered install path: {rendered}")
    return candidate.as_posix()


def _overlay_files(
    build_root: Path, modules: tuple[str, ...] | None
) -> tuple[dict[str, Path], tuple[str, ...], tuple[ModuleSpec, ...]]:
    template = build_root / "core"
    if not template.is_dir():
        raise InstallError(f"Build has no core directory: {template}")
    files: dict[str, Path] = {}
    for path in template.rglob("*"):
        if not path.is_file():
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(template.resolve()):
            raise InstallError(f"Template contains an unsafe file: {path}")
        files[path.relative_to(template).as_posix()] = path
    catalog = load_module_catalog(build_root)
    specs_by_id = {spec.id: spec for spec in catalog}
    available_modules = build_root / "modules"
    selected_modules = modules
    if selected_modules is None:
        selected_modules = tuple(spec.id for spec in catalog)
    else:
        selected_modules = tuple(dict.fromkeys(selected_modules))
    for module in selected_modules:
        if module not in specs_by_id:
            raise InstallError(f"Unknown module: {module}")
        payload = available_modules / module / "payload"
        if not payload.is_dir():
            raise InstallError(f"Unknown or empty module: {module}")
        for path in sorted(item for item in payload.rglob("*") if item.is_file()):
            if path.is_symlink() or not path.resolve().is_relative_to(payload.resolve()):
                raise InstallError(f"Module {module} contains an unsafe file: {path}")
            relative = path.relative_to(payload).as_posix()
            if relative in files:
                raise InstallError(f"Module {module} collides with another installed file: {relative}")
            files[relative] = path
    return files, selected_modules, tuple(specs_by_id[module] for module in selected_modules)


def _module_navigation(specs: tuple[ModuleSpec, ...]) -> tuple[str, str]:
    if not specs:
        return "Keine optionalen Module installiert.", "Keine"
    navigation = "\n".join(f"- [[{spec.entry}]] – {spec.title}" for spec in specs)
    return navigation, ", ".join(spec.title for spec in specs)


def rebuild_installed_data_model(staging: Path) -> None:
    runtime = staging / "system/data-model/scripts/pos_v1.py"
    if not runtime.is_file():
        return
    try:
        subprocess.run(
            [sys.executable, str(runtime), "--root", str(staging), "build"],
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        raise InstallError(f"Installed data-model build failed: {detail.strip()}") from exc


def install_personalos(config: InstallConfig) -> InstallResult:
    if config.destination.exists():
        if not config.destination.is_dir():
            raise InstallError(f"Destination exists but is not a directory: {config.destination}")
        if any(config.destination.iterdir()):
            raise InstallError(f"Destination is not empty: {config.destination}")
    integrity = audit_build(config.build_root, [])
    if not integrity.ok:
        first = integrity.findings[0]
        raise InstallError(f"Build audit failed: {first.code} {first.path} {first.detail}")
    files, selected_modules, selected_specs = _overlay_files(config.build_root, config.modules)
    values = _default_values(config.destination)
    values.update(config.values)
    _validate_human_values(values)
    user_name = values.get("user_name", "").strip()
    if user_name:
        values["user_name"] = user_name
    values.setdefault("user_slug", re.sub(r"[^a-z0-9]+", "-", user_name.casefold()).strip("-"))
    values.setdefault("user_last_name", user_name.rsplit(" ", 1)[-1])
    _validate_slug_values(values)
    module_navigation, module_summary = _module_navigation(selected_specs)
    values["installed_modules_navigation"] = module_navigation
    values["installed_modules_summary"] = module_summary
    install_date = values.get("install_date", "")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", install_date):
        raise InstallError(f"Invalid install_date: {install_date}")
    try:
        date.fromisoformat(install_date)
    except ValueError:
        raise InstallError(f"Invalid install_date: {install_date}")
    if "install_year" not in config.values:
        values["install_year"] = install_date[:4]
    elif values["install_year"] != install_date[:4]:
        raise InstallError("install_year must match install_date")
    ids: dict[str, str] = {}

    config.destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{config.destination.name}-install-", dir=config.destination.parent)
    )
    try:
        rendered_paths: set[str] = set()
        for relative, source in sorted(files.items()):
            rendered_relative = _render_relative_path(relative, values, ids)
            if rendered_relative in rendered_paths:
                raise InstallError(f"Rendered install path collision: {rendered_relative}")
            rendered_paths.add(rendered_relative)
            destination = staging / rendered_relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            content = source.read_bytes()
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                destination.write_bytes(content)
                continue
            _assert_safe_executable_template(relative, text)
            destination.write_text(_render_text(text, values, ids), encoding="utf-8")
        if config.rebuild_data_model:
            rebuild_installed_data_model(staging)
        if config.destination.exists():
            config.destination.rmdir()
        os.replace(staging, config.destination)
        return InstallResult(
            destination=config.destination,
            modules=selected_modules,
            file_count=len(files),
        )
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
