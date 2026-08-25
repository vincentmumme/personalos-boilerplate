---
schema_version: pos-v1
id: 01a0011a-dabc-7243-961a-cd9155dfcb97
type: data-model-document
title: "pos-v1 Registry Governance"
created: 2026-08-10
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
document_kind: registry-governance
---

# pos-v1 Registry Governance

## Current Truth

`system/data-model/governance.yaml` ist der maschinenlesbare Vertrag dafür, wie Page Shapes, Module, Primary Profiles und Felder in `pos-v1` aufgenommen, aktiviert, verändert, deprecated und entfernt werden. Eine einzelne Instanz, ein Skill oder ein Domainordner darf den Contract nicht eigenständig erweitern.

Diese Datei erklärt den Vertrag für Menschen. Bei Abweichungen gilt die YAML-Registry gemeinsam mit der zugrunde liegenden Architekturentscheidung.

## Admission

Ein neues Profile benötigt mindestens:

1. einen nachweisbaren semantischen Bedarf, der nicht durch ein bestehendes Profile plus kontrolliertes Feld abgedeckt wird;
2. genau einen Page Shape und kanonischen Owner;
3. erlaubte Roots und einen deterministischen Pfadvertrag nach [[system/conventions/core/record-naming-and-temporal-paths]]; zeitliche Partitionierung wird pro Record-Familie ausdrücklich festgelegt und nie spontan aus Bestandsgröße abgeleitet;
4. vollständig registrierte Pflicht-/optionale Felder und Module;
5. Body Sections und ein normatives Template;
6. positive und negative Fixtures sowie Validator-Coverage;
7. ein Legacy-/Migrationsmapping, sofern Bestand betroffen ist;
8. Registry-Eintrag und Activation State.

Module benötigen kohärente wiederverwendbare Semantik und grundsätzlich mindestens zwei aktive Consumer. Ein Pilotmodul mit weniger Consumern muss geplante Consumer ausweisen und darf nicht still als dauerhaft universell behandelt werden. Ein Feld wird nur aufgenommen, wenn es atomaren Query-, Routing-, Relationship-, State- oder Validierungswert besitzt, genau einen semantischen Owner hat und nicht besser in Body oder Companion Data gehört.

## Activation States

| State | Bedeutung | Neue Writes |
|---|---|---:|
| `draft` | Contract wird entworfen und ist nicht instanzfähig | nein |
| `pilot` | vollständiger Contract mit grünen Fixtures und begrenztem realem Einsatz | ja |
| `active` | stabiler produktiver Contract mit repräsentativen Records und Migrationspfad | ja |
| `read-only` | bestehende Records bleiben lesbar; Writer sind deaktiviert | nein |
| `deprecated` | Ersatz und Migration sind angekündigt; keine neuen Instanzen | nein |
| `retired` | keine aktiven Records; nur Receipt beziehungsweise historische Lesbarkeit | nein |

`profile_states` in `registry.yaml` ist die einzige Aktivierungswahrheit. Writable Profiles werden daraus anhand der in `governance.yaml` erlaubten States abgeleitet; eine separate manuell gepflegte Allowlist existiert nicht.

## Change Classes

| Klasse | Beispiele | Version/Migration |
|---|---|---|
| `corrective` | Dokumentations- oder Validatorfix ohne Contractänderung | Patch-Version, keine Migration |
| `additive` | neues Profile/Modul, optionales Feld, erweitertes Enum | Minor-Version, bestehende Records bleiben gültig |
| `deprecation` | kontrolliertes Auslaufen von Feld, Modul oder Profile | Minor-Version plus Ersatz- und Migrationsvertrag |
| `breaking` | Feldentfernung, neue nicht ableitbare Pflicht, Typ-/Kardinalitäts-/Semantik- oder Page-Shape-Wechsel | neue Contract-Generation oder vorgelagerte vollständige Migration |

## Deprecation

Jede Deprecation benötigt Ersatz, Begründung, Ankündigungsdatum, Write Policy und Migration Reference in `deprecations.yaml`. Stilles Entfernen ist verboten. `deprecated` beziehungsweise `read-only` deaktiviert neue Writes, ohne bestehende Records unlesbar zu machen.

## Atomic Release

Eine Contractänderung ist erst vollständig, wenn Registry, Foundation/Governance, Page Shapes, Module, Profiles, Templates, Runtime, Fixtures, Generated Views und Changelog gemeinsam konsistent sind. `pos-verify` blockiert Registryänderungen mit Generated-Drift. Der Generated Manifest Fingerprint bindet die abgeleiteten Artefakte an ihre kanonischen YAML-Quellen.

## Timeline

- **2026-08-10** | Admission-, Activation-, Change-Class-, Deprecation- und Atomic-Release-Vertrag als Registry Governance `1.0.0` materialisiert.
- **2026-08-11** | Menschliche Admission-Erläuterung an den POS-weiten Naming- und Temporal-Path-Vertrag gebunden; der maschinenlesbare Profile-Pfadvertrag bleibt `path_pattern`.
