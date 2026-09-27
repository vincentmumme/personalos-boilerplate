"""Shared rules for the folder that receives a new PersonalOS installation."""
from __future__ import annotations

import errno
import os
from pathlib import Path

# Tools create these entries as soon as a user prepares the folder, for example by
# opening it as an Obsidian vault or viewing it in Finder or Explorer. They hold no
# personal truth, so a folder containing only them still counts as a new target.
# The installed system already treats `.obsidian/` as a technical root exception.
PREPARED_ENTRY_NAMES = frozenset({".obsidian", ".ds_store", "thumbs.db", "desktop.ini"})
PREPARED_ENTRIES_HINT = "Nur `.obsidian/` und Systemdateien wie `.DS_Store` dürfen schon vorhanden sein."


def is_prepared_entry(path: Path) -> bool:
    return path.name.casefold() in PREPARED_ENTRY_NAMES


def blocking_entries(destination: Path) -> list[Path]:
    """Entries that make an existing folder unsuitable for a new installation."""
    if not destination.is_dir():
        return []
    return sorted(path for path in destination.iterdir() if not is_prepared_entry(path))


def prepared_entries(destination: Path) -> list[Path]:
    if not destination.is_dir():
        return []
    return sorted(path for path in destination.iterdir() if is_prepared_entry(path))


def hand_over(staging: Path, destination: Path) -> None:
    """Move a finished staging tree into place.

    An empty or missing destination is replaced in one step. A prepared destination keeps
    its own entries and its identity, so an open Obsidian vault stays the same folder: the
    installed entries move in one by one and are moved back if a later move fails.
    """
    if not destination.exists():
        os.replace(staging, destination)
        return
    present = sorted(destination.iterdir())
    if any(not is_prepared_entry(path) for path in present):
        raise OSError(errno.ENOTEMPTY, "Destination is not empty", str(destination))
    if not present:
        destination.rmdir()
        os.replace(staging, destination)
        return
    incoming = sorted(staging.iterdir())
    for path in incoming:
        if os.path.lexists(destination / path.name):
            raise OSError(errno.EEXIST, "Installed entry collides with a prepared entry", str(destination / path.name))
    moved: list[str] = []
    try:
        for path in incoming:
            os.replace(path, destination / path.name)
            moved.append(path.name)
    except OSError:
        for name in reversed(moved):
            try:
                os.replace(destination / name, staging / name)
            except OSError:
                pass
        raise
    try:
        staging.rmdir()
    except OSError:
        pass
