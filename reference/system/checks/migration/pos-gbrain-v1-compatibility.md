---
schema_version: pos-v1
id: 019fec98-259e-797d-98e1-3d149c53d05c
type: check
title: "pos-gbrain-v1 Compatibility"
created: 2026-08-10
updated: 2026-08-22
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/personalos-mutation-contract]]", "[[system/frameworks/core/verification-ownership]]"]
check_kind: migration
verifies_refs: ["[[system/contracts/core/personalos-mutation-contract]]", "[[system/frameworks/core/verification-ownership]]"]
---

# pos-gbrain-v1 Compatibility

## Purpose

Dieser befristete Check besitzt alle noch erforderlichen Compatibility-Assertions für klassifizierte historische `pos-gbrain-v1`-Records und Legacy-Skill-Referenzen. Er ist ein Retention- und Lesbarkeitsguard, kein Hinweis auf eine offene aktive Domainmigration.

## Assertions

- Ein bereits kanonisch migrierter Zielpfad fällt nicht unbemerkt auf ein Legacy-Schema zurück.
- Klassifizierte Legacy-Records behalten die für ihre historische Lesbarkeit erforderlichen Shape-Grenzen.
- Historische Automation-Output-Shapes bleiben lesbar und prüfbar, ohne einen neuen Writer oder einen zukünftigen Pflicht-Cutover zu begründen.
- Legacy-Skills verletzen die bestehende Mutation Loop oder Systemautorität nicht unbemerkt.
- Jede Assertion bleibt als Migration Compatibility markiert und wird nicht zur neuen Zielnorm erhoben.

## Implementation

Die Funktionen leben gebündelt in `skills/pos-verify/scripts/run.py`. Ihre Finding Codes sind in `system/checks/core/verification-ownership.json` diesem Check zugeordnet. Eine Assertion wird erst entfernt, wenn kein klassifizierter historischer Bestand oder Consumer sie mehr benötigt und ein grüner Ersatzcheck existiert oder die alte Regel ausdrücklich retired wurde.

## Invocation

```bash
python3 skills/pos-verify/scripts/run.py --files <explizite-dateiliste>
```

## Outcomes

- `pass`: die betroffenen historischen Legacy-Records bleiben konsistent und nicht-autoritativ.
- `warn`: sichtbare ungeklärte Legacy- oder Klassifikationsschuld ohne unmittelbare Integritätsverletzung.
- `fail`: Legacy-Shape, kanonischer Zielpfad oder bestehende Sicherheitsgrenze ist verletzt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
