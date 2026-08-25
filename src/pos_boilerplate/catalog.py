from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


class ModuleCatalogError(ValueError):
    """Raised when the public module catalog and payload tree disagree."""


MODULE_ID_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


@dataclass(frozen=True)
class ModuleSpec:
    id: str
    kind: str
    title: str
    entry: str


def load_module_catalog(build_root: Path) -> tuple[ModuleSpec, ...]:
    catalog_path = build_root / "modules/catalog.json"
    try:
        raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ModuleCatalogError(f"Module catalog is missing or invalid: {catalog_path}") from exc
    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise ModuleCatalogError("Module catalog must use schema_version 1")
    raw_modules = raw.get("modules")
    if not isinstance(raw_modules, list):
        raise ModuleCatalogError("Module catalog must contain a modules list")

    specs: list[ModuleSpec] = []
    seen: set[str] = set()
    for item in raw_modules:
        if not isinstance(item, dict):
            raise ModuleCatalogError("Every module catalog entry must be an object")
        values = {key: item.get(key) for key in ("id", "kind", "title", "entry")}
        if not all(isinstance(value, str) and value for value in values.values()):
            raise ModuleCatalogError("Every module needs id, kind, title and entry")
        module_id = values["id"]
        if MODULE_ID_RE.fullmatch(module_id) is None or module_id in seen:
            raise ModuleCatalogError(f"Unsafe or duplicate module id: {module_id!r}")
        entry = values["entry"]
        if entry.startswith("/") or ".." in Path(entry).parts or "\\" in entry:
            raise ModuleCatalogError(f"Unsafe module entry: {entry!r}")
        seen.add(module_id)
        specs.append(ModuleSpec(module_id, values["kind"], values["title"], entry))

    default_enabled = raw.get("default_enabled", [])
    if not isinstance(default_enabled, list) or not all(
        isinstance(module_id, str) and module_id in seen for module_id in default_enabled
    ):
        raise ModuleCatalogError("default_enabled must contain only declared module ids")

    modules_root = build_root / "modules"
    payload_ids = {
        path.name
        for path in modules_root.iterdir()
        if path.is_dir() and (path / "payload").is_dir()
    } if modules_root.is_dir() else set()
    if seen != payload_ids:
        missing = sorted(seen - payload_ids)
        undeclared = sorted(payload_ids - seen)
        raise ModuleCatalogError(
            f"Module catalog and payloads differ; missing={missing}, undeclared={undeclared}"
        )
    return tuple(specs)
