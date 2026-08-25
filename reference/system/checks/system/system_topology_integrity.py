#!/usr/bin/env python3
"""Validate materialized PersonalOS system-topology records."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "system/data-model/scripts/pos_v1.py"
PROFILES = {
    "agent",
    "agent-persona-overlay",
    "runtime",
    "host",
    "system-service",
    "integration",
    "access-record",
    "operating-system",
    "view-record",
    "system-observability-view",
}
SEARCH_ROOTS = (
    "system/agents",
    "system/runtimes",
    "system/hosts",
    "system/services",
    "system/integrations",
    "system/access",
    "system/operating-systems",
    "system/views",
    "system/observability",
)
FORBIDDEN_ACCESS_KEYS = re.compile(
    r"^(?:secret|secret_value|token|password|api_key|private_key):",
    re.I | re.M,
)


def load_runtime():
    spec = importlib.util.spec_from_file_location("system_topology_runtime", RUNTIME)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    runtime = load_runtime()
    contract = runtime.Contract(ROOT)
    failures: list[str] = []
    checked = 0
    for relative_root in SEARCH_ROOTS:
        root = ROOT / relative_root
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            try:
                frontmatter, _, _ = runtime.split_markdown(text)
            except runtime.ContractError:
                continue
            if frontmatter.get("schema_version") != "pos-v1" or frontmatter.get("type") not in PROFILES:
                continue
            checked += 1
            for finding in contract.validate_file(path, check_duplicate_ids=False):
                if finding.level == "fail":
                    failures.append(f"{path.relative_to(ROOT)}:{finding.code}:{finding.message}")
            if frontmatter.get("type") == "access-record":
                block = text[4 : text.find("\n---\n", 4)]
                if FORBIDDEN_ACCESS_KEYS.search(block):
                    failures.append(f"{path.relative_to(ROOT)}:access_secret_key")
    if failures:
        print("system-topology-integrity: fail")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"system-topology-integrity: pass ({checked} record(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
