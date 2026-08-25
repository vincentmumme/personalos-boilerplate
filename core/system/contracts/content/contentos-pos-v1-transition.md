---
schema_version: pos-v1
id: 019ff134-cc0b-7155-8007-f9063fadf116
type: contract
title: "ContentOS to pos-v1 Transition"
created: 2026-08-11
updated: 2026-08-15
lifecycle: retired
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# ContentOS to pos-v1 Transition

## Contract

Der Übergang ist abgeschlossen. `pos-v1` ist der einzige aktive Vertrag für ContentOS-Records. Die registrierten `content-*` Primary Profiles, das Modul `content-core`, die zentralen System-Contracts und Templates sowie der `contentos`-Skill bilden gemeinsam den produktiven Zielzustand. Dieser Record bleibt ausschließlich als historischer Übergangsbeleg erhalten.

## Scope

Der historische Scope umfasste alle ContentOS-Records unter `content/`, Content-Knowledge-Candidates, den `contentos`-Skill, Validatoren, Capabilities, Templates, Contracts, IDs und interne Links. Die operative Wahrheit liegt nun in Registry, Zielprofilen und den Content-System-Contracts.

## Invariants

- Jeder migrierte Content-Record erhält die universelle sechs-Felder-Foundation `schema_version`, `id`, `type`, `title`, `created`, `updated`.
- Content-spezifische Identität, Beziehungen, State Machines, Revision, Concurrency, Execution, Provenance, Publication und Evidence werden ausschließlich durch das jeweilige Content-Profile und registrierte Module ergänzt.
- `cos_object_type` und `role` werden im Ziel durch genau ein semantisches Primary Profile ersetzt; `cos_schema_version` entfällt nach dem atomaren Cutover.
- Das heutige `status` wird profilespezifisch in `maturity`, `lifecycle`, `phase`, `*_state` und `*_outcome` zerlegt.
- Die globale UUIDv7-`id` wird zur POS-Record-Identität. Bestehende `cos_id`-Werte bleiben im Migration Receipt als Legacy-Zuordnung erhalten; alle Beziehungen werden atomar auf die neuen IDs abgebildet. Kein Writer improvisiert vor Admission ein zusätzliches ID-Feld.
- `revision` und optimistic locking bleiben für mutable Content-Records erhalten und werden über ein zugelassenes Revision-/Concurrency-Modul modelliert.
- Alle aktiven Writer schreiben ausschließlich registrierte `pos-v1`-Content-Profile; ein Legacy- oder Dual-Write-Pfad ist nicht zulässig.
- Der Cutover ist atomar über Registry, Profile, Module, Templates, Validatoren, Capabilities, IDs, Links, Fixtures und Recovery. Dual Writes und parallele aktive Contentwahrheiten sind verboten.

## Interfaces

```text
pos-v1 Foundation
  + genau ein Content Primary Profile
  + registrierte Content-/Lifecycle-/Knowledge-Module
  -> globale Registry Runtime + Content-spezifische Checks
```

Das bestehende Content-Objektmodell bestimmt die fachlichen Objektgrenzen und Lifecycles. Der globale Frontmatter-Vertrag bestimmt Foundation, Feldownership, Profile-Admission, Page Shape und Cutover-Disziplin. Bei der Migration wird Fachsemantik erhalten, aber ihre technische Repräsentation in die globale Registry überführt.

## Compliance

Ein Content-Write ist nur compliant, wenn sein Profile in `system/data-model/registry.yaml` `pilot` oder `active` ist und der Record den zugehörigen Template-, Path-, Module- und Check-Vertrag erfüllt.

Es ist nicht compliant, die sechs Foundation-Felder einfach auf heutige COS-Dateien aufzusetzen, `cos_id` ohne vollständige Relationsmigration zu entfernen, beide Schemas parallel aktiv zu schreiben oder Content-Profile ad hoc in einem Skill zu definieren.

## Evolution

Dieser Übergangsvertrag ist retired. Änderungen am laufenden ContentOS erfolgen ab jetzt über die kanonischen Content-Contracts, die globale Registry und explizite Migration Receipts.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
