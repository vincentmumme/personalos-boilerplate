from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class PlatformTests(unittest.TestCase):
    def test_git_checkout_preserves_hashed_text_with_autocrlf_enabled(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        fixtures = {
            "core/USER.md": b"# User\n\nName: {{user_name}}\n",
            "core/hook": b"#!/bin/sh\necho public\n",
            "modules/sample/payload/data.fixture": b"first\nsecond\n",
            "core/binary.bin": b"\x00\x01\r\n\xff",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            def git(*args: str) -> None:
                subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)

            git("init", "-q")
            git("config", "core.autocrlf", "true")
            git("config", "core.safecrlf", "false")
            attributes = repository / ".gitattributes"
            if attributes.is_file():
                (root / ".gitattributes").write_bytes(attributes.read_bytes())
            for relative, content in fixtures.items():
                file = root / relative
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(content)
            git("add", ".")
            for relative in fixtures:
                (root / relative).unlink()
            git("checkout-index", "--all", "--force")

            for relative, content in fixtures.items():
                with self.subTest(path=relative):
                    self.assertEqual((root / relative).read_bytes(), content)

    def test_iana_timezone_works_without_an_operating_system_database(self) -> None:
        # Windows generally has no system IANA database. Exercise the package
        # fallback on every runner without changing the process-global TZPATH.
        result = subprocess.run(
            [sys.executable, "-c", (
                "from datetime import datetime; "
                "from zoneinfo import ZoneInfo; "
                "print(datetime(2026, 6, 1, tzinfo=ZoneInfo('Europe/Berlin')).utcoffset())"
            )],
            env={**os.environ, "PYTHONTZPATH": ""},
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "2:00:00")


if __name__ == "__main__":
    unittest.main()
