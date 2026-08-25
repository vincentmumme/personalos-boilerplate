---
schema_version: pos-v1
id: 019fec98-2544-789e-a509-6cb7c166ce9f
type: check
title: "Markdown Record Integrity"
created: 2026-08-10
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/normative-system-architecture]]", "[[system/contracts/core/personalos-mutation-contract]]", "[[system/contracts/core/internal-links-and-path-mutations]]", "[[system/conventions/core/record-naming-and-temporal-paths]]"]
check_kind: content
verifies_refs: ["[[system/contracts/normative-system-architecture]]", "[[system/contracts/core/personalos-mutation-contract]]", "[[system/contracts/core/internal-links-and-path-mutations]]", "[[system/conventions/core/record-naming-and-temporal-paths]]"]
---

# Markdown Record Integrity

## Purpose

Dieser Check besitzt die format- und graphbezogenen Baseline-Assertions für geänderte PersonalOS-Markdown-Dateien unabhängig vom konkreten Primary Profile.

## Assertions

- POS-Markdown-Records besitzen parsebares Frontmatter, sofern ihr Vertrag keine technische Ausnahme zulässt.
- YAML-Listen folgen der kanonischen, deterministisch parsebaren Schreibweise.
- Neue `pos-v1`-Records erfüllen den registrierten Pfadvertrag; semantische Slugs, UUID-Dateinamen und Datumsbestandteile folgen der Naming Convention des Profiles.
- Interne Wikilinks sind eindeutig auflösbar oder ausdrücklich als zulässiger externer beziehungsweise zukünftiger Target klassifiziert.
- Geänderte Dateien führen weder kaputte noch mehrdeutige Links neu ein.
- Bei Moves und Renames bleiben UUID und kontrollierbare Inbound-Links konsistent; Redirects ersetzen keinen vollständigen Linkplan.

## Implementation

Die ausführbare Implementierung liegt während des Bootstrap-Cutovers in `system/data-model/scripts/pos_v1.py` für registrierte Profile und in wiederverwendbaren Funktionen von `skills/pos-verify/scripts/run.py` für Markdown- und Linkintegrität. Die Funktionen dürfen keine profilgebundene Feld-, Body- oder Owner-Semantik erfinden; repositoryweite Move-Manifeste ergänzen den write-scoped Check bei Pfadmigrationen.

## Invocation

```bash
python3 skills/pos-verify/scripts/run.py --files <explizite-dateiliste>
```

## Outcomes

- `pass`: Frontmatter und Links erfüllen die generische Markdown-Baseline.
- `warn`: ein Link ist bewusst noch nicht materialisiert oder eine Legacy-Ausnahme bleibt sichtbar.
- `fail`: Frontmatter fehlt, eine Listenform ist nicht kanonisch oder ein interner Link ist kaputt beziehungsweise mehrdeutig.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
