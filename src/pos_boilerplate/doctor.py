"""Read-only checks for a new installation or an existing user's folder."""
from __future__ import annotations

import os
import platform
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .audit import audit_build


@dataclass(frozen=True)
class EnvironmentCheck:
    code: str
    status: str
    message: str
    remedy: str = ""


@dataclass(frozen=True)
class EnvironmentReport:
    mode: str
    checks: tuple[EnvironmentCheck, ...]

    @property
    def ok(self) -> bool:
        return all(item.status != "fail" for item in self.checks)

    def to_dict(self) -> dict:
        return {"ok": self.ok, "mode": self.mode, "checks": [asdict(item) for item in self.checks]}


def _check_destination(build_root: Path, destination: Path, mode: str) -> list[EnvironmentCheck]:
    if destination.is_symlink():
        return [EnvironmentCheck(
            "destination-symlink", "fail", "Der Zielordner ist ein symbolischer Link.",
            "Den tatsächlichen Zielordner bewusst auswählen und den Check erneut ausführen.",
        )]
    if destination.resolve().is_relative_to(build_root.resolve()):
        return [EnvironmentCheck(
            "destination-in-build", "fail", "Der Zielordner liegt innerhalb der Boilerplate.",
            "Einen eigenen Ordner außerhalb des heruntergeladenen Repositorys wählen.",
        )]
    if destination.exists() and not destination.is_dir():
        return [EnvironmentCheck(
            "destination-type", "fail", "Am Ziel liegt eine Datei.",
            "Einen Ordnerpfad wählen; die vorhandene Datei bleibt erhalten.",
        )]
    if mode == "existing":
        if not destination.is_dir():
            return [EnvironmentCheck(
                "destination-missing", "fail", "Der bestehende Ordner wurde nicht gefunden.",
                "Den tatsächlichen Pfad prüfen. Für ein neues System --mode new verwenden.",
            )]
        # Deliberately do not inspect private contents or execute the existing system.
        if not os.access(destination, os.R_OK | os.X_OK):
            return [EnvironmentCheck(
                "destination-access", "fail", "Der bestehende Ordner ist nicht lesbar.",
                "Dem Agenten gezielt Zugriff auf diesen Ordner erlauben.",
            )]
        return [EnvironmentCheck(
            "existing-system", "pass", "Bestehender Ordner für eine lesende Bestandsaufnahme gefunden.",
            "Vor Änderungen Sicherung und Übernahmeplan klären. Den Installer nicht auf diesen Ordner anwenden.",
        )]
    if destination.exists() and any(destination.iterdir()):
        return [EnvironmentCheck(
            "destination-not-empty", "fail", "Der Zielordner enthält bereits Dateien.",
            "Einen leeren neuen Ordner wählen oder --mode existing zur Bestandsaufnahme verwenden.",
        )]
    parent = destination.parent
    while not parent.exists() and parent != parent.parent:
        parent = parent.parent
    if not parent.is_dir() or not os.access(parent, os.W_OK | os.X_OK):
        return [EnvironmentCheck(
            "destination-access", "fail", "Der übergeordnete Ordner ist nicht zugänglich oder beschreibbar.",
            "Einen beschreibbaren persönlichen Ordner wählen oder dessen Zugriffsrechte prüfen.",
        )]
    return [EnvironmentCheck(
        "destination", "pass", "Der neue Zielordner ist frei; die gemeldeten Schreibrechte passen.",
        "Es wurde keine Datei angelegt. Tatsächliche Schreibfähigkeit wird erst bei der Installation bestätigt.",
    )]


def check_environment(
    build_root: Path,
    destination: Path | None = None,
    *,
    mode: str = "new",
    timezone_name: str = "UTC",
) -> EnvironmentReport:
    """Diagnose without creating files, accessing accounts, or reading private records."""
    if mode not in {"new", "existing"}:
        raise ValueError("mode must be new or existing")
    checks = [
        EnvironmentCheck(
            "python", "pass" if sys.version_info >= (3, 11) else "fail",
            f"Python {platform.python_version()}; benötigt wird mindestens 3.11.",
            "Den dokumentierten Python-Interpreter und dessen virtuelle Umgebung verwenden.",
        ),
    ]
    supported = platform.system() in {"Darwin", "Linux", "Windows"}
    checks.append(EnvironmentCheck(
        "platform", "pass" if supported else "warn",
        f"Plattform: {platform.system() or 'unbekannt'}.",
        "" if supported else "Diese Plattform ist nicht Teil der vorgesehenen Testmatrix.",
    ))
    try:
        ZoneInfo(timezone_name)
        checks.append(EnvironmentCheck("timezone", "pass", "Die gewählte IANA-Zeitzone ist verfügbar."))
    except (ZoneInfoNotFoundError, ValueError):
        checks.append(EnvironmentCheck(
            "timezone", "fail", "Die angegebene Zeitzone ist ungültig oder ihre Daten fehlen.",
            "Eine IANA-Zone wie Europe/Berlin wählen. Bei fehlenden Daten mit demselben Python "
            "'-m pip install tzdata' ausführen; auch spätere POS-Prüfungen brauchen diese Umgebung.",
        ))
    git_available = shutil.which("git") is not None
    checks.append(EnvironmentCheck(
        "git", "pass" if git_available else "warn",
        "Git ist verfügbar." if git_available else "Git wurde nicht gefunden.",
        "Ein entpackter ZIP-Download lässt sich auch ohne Git installieren. Für Clone, "
        "Git-Historie oder Git-Sicherung Git gesondert einrichten.",
    ))
    try:
        integrity = audit_build(build_root, [])
        if integrity.ok:
            checks.append(EnvironmentCheck("build-integrity", "pass", "Build-Manifest, Module und interne Links sind konsistent."))
        else:
            # A stable code is sufficient; never echo arbitrary file contents or paths.
            code = integrity.findings[0].code
            checks.append(EnvironmentCheck(
                "build-integrity", "fail", f"Die heruntergeladene Vorlage ist nicht konsistent ({code}).",
                "Einen vollständigen aktuellen ZIP-Download neu entpacken oder frisch klonen. "
                "Bei manifest-hash-mismatch auch die Git-Zeilenenden prüfen; nicht den Hashcheck umgehen.",
            ))
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        checks.append(EnvironmentCheck(
            "build-integrity", "fail", "Die Vorlage konnte nicht vollständig gelesen werden.",
            "--build muss auf den entpackten Repository-Ordner mit manifest.json und core zeigen.",
        ))
    if destination is None:
        checks.append(EnvironmentCheck(
            "destination", "fail" if mode == "existing" else "warn", "Noch kein Zielordner geprüft.",
            "Den privaten Zielordner mit --destination angeben.",
        ))
    else:
        try:
            checks.extend(_check_destination(build_root, destination, mode))
        except (OSError, ValueError, RuntimeError):
            checks.append(EnvironmentCheck(
                "destination-access", "fail", "Der Zielpfad konnte nicht sicher geprüft werden.",
                "Pfad, Verknüpfungen und Zugriffsrechte prüfen; es wurden keine Dateien verändert.",
            ))
    checks.append(EnvironmentCheck(
        "agent-access", "warn",
        "Anmeldung, Modellzugang, Kosten, Agentenrechte und Sicherung wurden nicht automatisch geprüft.",
        "Diese Punkte im Onboarding klären; der technische Vorabcheck ersetzt keinen erfolgreichen Arbeitsablauf.",
    ))
    return EnvironmentReport(mode, tuple(checks))
