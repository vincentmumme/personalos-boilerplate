---
schema_version: pos-v1
id: 019ffb27-0d25-7a1a-acd2-ac265c4904ea
type: check
title: "Bootstrap und Portabilität Check"
created: 2026-08-13
updated: 2026-08-22
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/bootstrap-und-portabilitaet]]"]
check_kind: content
verifies_refs: ["[[system/contracts/core/bootstrap-und-portabilitaet]]", "[[system/templates/core/bootstrap/agent-entry]]", "[[system/templates/core/bootstrap/claude-adapter]]", "[[system/templates/core/bootstrap/root-index]]", "[[system/templates/core/bootstrap/user-context]]", "[[system/templates/core/bootstrap/agent-persona]]"]
---

# Bootstrap und Portabilität Check

## Purpose

Der Check beweist, dass Root-Bootstrap und technische Adapter aus portablen normativen Templates erzeugt werden können, ohne persönliche Instanzwerte oder Schattenregeln in die Boilerplate zu übernehmen.

## Assertions

- Vier Bootstrap-Profile sind vollständig registriert und writable.
- Fünf normative Templates rendern ohne nicht aufgelöste Pflichtplatzhalter.
- Portierbare Blueprints enthalten keine persönlichen Namen oder Companywerte aus {{user_name}}s Instanz.
- Neutrale und {{user_name}}-spezifische Fixtures erfüllen denselben Profilvertrag.
- `CLAUDE.md` enthält ausschließlich den Pointer auf `AGENTS.md`; jeder zusätzliche Inhaltsblock scheitert.
- Materialisierte Root-Records besitzen das erwartete Profil, den erlaubten Pfad und einen validen Body Shape.

## Implementation

Die portable Prüfung nutzt die öffentliche Registry-Laufzeit und den mitgelieferten Registry-Vertrag. Instanzspezifische Bootstrap-Ableitungen gehören nicht in die Boilerplate.

## Invocation

```bash
python3 system/data-model/scripts/pos_v1.py --root . check-registry
python3 -m unittest discover -s system/data-model/tests -p 'test_registry_contract.py'
```

Für die materialisierten Root-Records zusätzlich:

```bash
python3 system/data-model/scripts/pos_v1.py --root . validate --files AGENTS.md INDEX.md USER.md SOUL.md --json
```

## Outcomes

Persönliche Instanzwerte in portablen Blueprints, zusätzliche Adapterregeln, fehlende Pflichtpointer, nicht aufgelöste Platzhalter oder ein falsches Root-Profil sind blockierend.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
