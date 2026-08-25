---
schema_version: pos-v1
id: 019fec5e-7ffc-737a-9f5e-cfed4061b1a3
type: check
title: "pos-v1 Contract Check"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]"]
check_kind: schema
verifies_refs: ["[[system/contracts/normative-system-architecture]]"]
---

# pos-v1 Contract Check

## Purpose

Der Check stellt sicher, dass Registry, Foundation, Governance, Page Shapes, Module, Profiles, Templates, Fixtures und Generated Views gemeinsam einen ausführbaren, widerspruchsfreien `pos-v1`-Contract bilden.

## Assertions

- Profile und Module erfüllen den Admission-Vertrag.
- Jedes Feld besitzt genau einen semantischen Owner.
- Positive Fixtures bestehen und negative Fixtures scheitern.
- Templates, Pfade, Sections, Datentypen, Relationsziele und Profile States sind registriert.
- Generated Views stimmen mit ihren kanonischen YAML-Quellen überein.

## Implementation

Die kanonische Runtime liegt unter `system/data-model/scripts/pos_v1.py`; die fokussierte Testsuite unter `system/data-model/tests/test_registry_contract.py`.

## Invocation

```bash
python3 system/data-model/scripts/pos_v1.py --root . check-registry
python3 system/data-model/scripts/pos_v1.py build --check
python3 -m unittest discover -s system/data-model/tests -p 'test_registry_contract.py'
```

## Outcomes

Ein Contract-/Fixture-/Generated-Drift ist blockierend. Legacy-Relationswarnungen sind nur während einer ausdrücklich dokumentierten Migrationswelle zulässig.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
