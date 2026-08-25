from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNTIME_PATH = ROOT / "system" / "data-model" / "scripts" / "pos_v1.py"


def load_runtime():
    spec = importlib.util.spec_from_file_location("public_pos_v1_runtime", RUNTIME_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {RUNTIME_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runtime = load_runtime()


class PublicRegistryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = runtime.Contract(ROOT)

    def test_registry_and_all_admission_fixtures_pass(self) -> None:
        self.assertGreater(len(self.contract.profiles), 0)

    def test_generated_artifacts_match_the_registry(self) -> None:
        self.assertEqual([], self.contract.build_generated(check=True))


if __name__ == "__main__":
    unittest.main()
