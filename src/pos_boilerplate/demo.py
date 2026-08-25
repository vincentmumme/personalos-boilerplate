from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .install import (
    InstallConfig,
    InstallError,
    install_personalos,
    rebuild_installed_data_model,
)


class DemoError(RuntimeError):
    """Wird ausgelöst, wenn die Aufnahme-Demo nicht sicher erstellt werden kann."""


@dataclass(frozen=True)
class DemoConfig:
    build_root: Path
    destination: Path
    values: dict[str, str]
    fixtures: Path


@dataclass(frozen=True)
class DemoResult:
    destination: Path
    modules: tuple[str, ...]
    file_count: int


def _fixture_files(fixtures: Path) -> tuple[Path, ...]:
    if not fixtures.is_dir():
        raise DemoError(f"Der Ordner mit den Demo-Beispieldaten existiert nicht: {fixtures}")
    root = fixtures.resolve()
    files: list[Path] = []
    for path in sorted(fixtures.rglob("*")):
        if path.is_symlink():
            raise DemoError(
                f"Die Demo-Beispieldaten enthalten einen symbolischen Link: {path}"
            )
        if not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            raise DemoError(
                f"Eine Demo-Beispieldatei liegt außerhalb des vorgesehenen Ordners: {path}"
            )
        relative = path.resolve().relative_to(root)
        if relative.is_relative_to(Path("system/data-model/scripts")):
            raise DemoError(
                "Eine Demo-Beispieldatei liegt in einem geschützten Pfad: "
                f"{relative.as_posix()}"
            )
        files.append(path)
    if not files:
        raise DemoError(f"Der Ordner mit den Demo-Beispieldaten ist leer: {fixtures}")
    return tuple(files)


def _validate_demo_records(destination: Path, fixture_paths: tuple[str, ...]) -> None:
    runtime = destination / "system/data-model/scripts/pos_v1.py"
    markdown_files = [path for path in fixture_paths if path.endswith(".md")]
    if not runtime.is_file() or not markdown_files:
        return
    try:
        subprocess.run(
            [
                sys.executable,
                str(runtime),
                "--root",
                str(destination),
                "validate",
                "--files",
                *markdown_files,
            ],
            cwd=destination,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        detail = getattr(exc, "stderr", "") or getattr(exc, "stdout", "") or str(exc)
        raise DemoError(
            f"Die Prüfung der Demo-Datensätze ist fehlgeschlagen: {detail.strip()}"
        ) from exc


def build_demo(config: DemoConfig) -> DemoResult:
    if config.destination.exists():
        if not config.destination.is_dir():
            raise DemoError(f"Das Ziel existiert, ist aber kein Ordner: {config.destination}")
        if any(config.destination.iterdir()):
            raise DemoError(f"Der Zielordner ist nicht leer: {config.destination}")

    fixtures = _fixture_files(config.fixtures)
    config.destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{config.destination.name}-demo-",
        dir=config.destination.parent,
        ignore_cleanup_errors=True,
    ) as staging_root_value:
        staging = Path(staging_root_value) / "PersonalOS"
        values = dict(config.values)
        values["personalos_root"] = str(config.destination)
        try:
            install = install_personalos(
                InstallConfig(
                    build_root=config.build_root,
                    destination=staging,
                    modules=None,
                    values=values,
                    rebuild_data_model=False,
                )
            )

            relative_paths: list[str] = []
            for source in fixtures:
                relative = source.relative_to(config.fixtures).as_posix()
                relative_paths.append(relative)
                target = staging / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

            rebuild_installed_data_model(staging)
            _validate_demo_records(staging, tuple(relative_paths))

            try:
                config.destination.rmdir()
            except FileNotFoundError:
                pass
            os.replace(staging, config.destination)
            return DemoResult(
                destination=config.destination,
                modules=install.modules,
                file_count=sum(1 for path in config.destination.rglob("*") if path.is_file()),
            )
        except InstallError as exc:
            raise DemoError(f"Die Demo konnte nicht erstellt werden: {exc}") from exc
