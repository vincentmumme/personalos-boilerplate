---
schema_version: pos-v1
id: 019fec8b-0c07-760c-a56d-827d0ed30b3a
type: check
title: "PersonalOS Mutation Postflight"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/personalos-mutation-contract]]", "[[system/frameworks/core/verification-ownership]]", "[[system/runbooks/core/personalos-mutation]]"]
check_kind: content
verifies_refs: ["[[system/contracts/core/personalos-mutation-contract]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]", "[[system/runbooks/core/personalos-mutation]]"]
---

# PersonalOS Mutation Postflight

## Purpose

Dieser Check deklariert den verbindlichen Postflight jeder POS-Mutation und trennt normative Assertions von der ausführenden Verification-Capability.

## Assertions

- Die geprüfte Menge entspricht der expliziten Liste dieses Writes; fremde Dirty-Tree-Änderungen werden nicht still zugerechnet.
- Jeder neue oder geänderte `pos-v1`-Record erfüllt Foundation, Profile, Module, Pfad, Body Shape, Relations und Registry State.
- Legacy-Records erfüllen die noch geltende Owner- und Shape-Grenze oder erzeugen eine sichtbare Migrationswarnung.
- Kein Konfliktmarker, nicht registriertes Feld, duplizierter stabiler Identifier oder blockierender Generated Drift bleibt bestehen.
- Neue Wahrheit liegt beim richtigen kanonischen Owner; Source, Interaction, Timeline, Daily Log, View, Run oder Todo sind nicht versehentlich zweite Current Truth.
- Plausible angrenzende Owner wurden als Update, Reference, No-op, Stage oder Ask beurteilt.
- Materielle Claims besitzen Provenance; sensible Daten und Secrets überschreiten ihre Boundary nicht.
- Current Truth wurde bei State-Änderung neu synthetisiert, Timeline nur bei echten Events oder Dateiänderungen ergänzt und Action Truth nicht als Schattenliste dupliziert.
- Moves und Deletes besitzen den erforderlichen Link-, Recovery- und Freigabenachweis.

## Implementation

Während des Bootstrap-Cutovers führt `skills/pos-verify/scripts/run.py` die write-scoped Baseline und `system/data-model/scripts/pos_v1.py` Registry-, Profile- und Generated-Checks aus. [[system/frameworks/core/verification-ownership]] ordnet jeden Finding Code einem deklarativen Owner zu; `system/checks/core/verification-ownership.json` prüft diese Zuordnung maschinenlesbar. Der `pos-verify`-Skill ergänzt die semantische Owner-/Propagation-Prüfung. Legacy-Hardcodings bleiben ausschließlich unter [[system/checks/migration/pos-gbrain-v1-compatibility]] sichtbar.

## Invocation

```bash
python3 skills/pos-verify/scripts/run.py --files <explizite-dateiliste>
```

Bei Registry-Änderungen zusätzlich:

```bash
python3 system/data-model/scripts/pos_v1.py --root . check-registry
python3 system/data-model/scripts/pos_v1.py build --check
python3 -m unittest discover -s system/data-model/tests -p 'test_registry_contract.py'
```

## Outcomes

- `pass`: deterministische Checks und semantisches Routing sind ohne relevante Finding abgeschlossen.
- `warn`: der Write ist nutzbar, aber benannte Legacy-, Relations-, Provenance- oder Migrationsschuld bleibt bestehen.
- `fail`: Shape, Owner, Konsistenz, Sicherheit, Generated Contract oder Verification ist blockierend verletzt.

Der Check erzeugt standardmäßig keinen dauerhaften Report. Ein persistierter Run Receipt entsteht nur, wenn das owning Profile oder die Automation ihn verlangt.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
