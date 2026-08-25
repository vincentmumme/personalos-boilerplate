---
schema_version: pos-v1
id: 019fec59-eec3-7fb2-947d-27bbd43453df
type: contract
title: "Normative System Architecture"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
supersedes_refs: ["[[system/contracts/normative-system-architecture]]"]
contract_version: 1.1.0
---

# Normative System Architecture

## Contract

Alle allgemeinen Principles, Rules, Contracts, Conventions, Frameworks, Data-Model-Definitionen, normativen Templates, systemweiten Runbooks und Checks des PersonalOS besitzen genau einen kanonischen Owner unter `system/`. Skills bleiben ausführbare Capabilities und dürfen keine konkurrierende allgemeine Systemverfassung besitzen.

## Scope

Der Contract gilt für alle POS-verwalteten Systemartefakte, Agenteneinstiege, Skills, Writer, Validatoren, Templates, Migrationen und generierten Systemansichten. Skillspezifische Ausführungslogik sowie skilllokale Referenzen und Assets dürfen beim Skill bleiben, solange sie keine allgemeine POS-Semantik definieren.

## Invariants

- Eine normative Aussage besitzt genau einen kanonischen Owner.
- Principles sind die höchste Ableitungsgrundlage; Rules und Contracts sind bindend.
- Conventions sind verbindliche Defaults mit ausdrücklich begründbarer Ausnahme.
- Frameworks strukturieren, erzeugen aber allein keine neue Pflicht.
- Data Model und Schema sind die maschinenlesbare Implementierung akzeptierter Contracts.
- Templates, Runbooks, Skills und Checks sind abgeleitet und dürfen keine fehlende Norm versteckt erfinden.
- Decisions autorisieren Änderungen, besitzen danach aber nicht die aktuelle Norm.
- Konflikte werden blockiert und niemals durch stillen Vorrang eines nachgelagerten Artefakts kaschiert.
- Normative Artefaktpfade folgen zuerst der Kategorie, danach dem Scope und nur bei echtem Bedarf einer Objektfamilie.
- Templates persistierter POS-Records liegen unter `system/templates/`; skilllokale Artefakte dürfen keine versteckten Record-Verträge bilden.

## Interfaces

```text
Decision + Evidence
        |
        v
Principle
  |----> Rule
  |----> Contract
  |----> Convention
  `----> Framework
             |
             +----> Data Model / Schema / Profile
             +----> Template
             +----> Runbook / Skill
             `----> Check
```

Consumer deklarieren direkte `system_refs`. Kontrolliert transitive Normabhängigkeiten und inverse Consumer-Views werden abgeleitet. Decision-/History-Links dienen Provenance und werden nicht standardmäßig in den Task-Kontext geladen.

Die physische Scope- und Capability-Grenze wird durch [[system/contracts/core/system-artifact-ownership-and-capability-boundary]] konkretisiert. Der Resolver bleibt der Intent-zu-Skill-Router; ein zusätzlicher allgemeiner POS-Router ist im Zielzustand nicht erforderlich.

## Compliance

Neue Systemartefakte werden ausschließlich über registrierte Primary Profiles, normative Templates, Admission-Fixtures und Checks aufgenommen. Unbekannte Abhängigkeiten, nicht registrierte Felder, konkurrierende Normowner und Drift zwischen Norm, Schema, Template, Skill oder Check blockieren neue Writes. Legacy-Consumer bleiben nur bis zu einem grünen Ersatz-Cutover aktiv.

## Evolution

Neue synonymfreie Kategorien benötigen einen semantischen Bedarf, den kein bestehender Typ plus kontrollierte Klassifikation abdeckt. Profil-, Modul-, Template-, Fixture-, Runtime-, Generated-View- und Migrationsänderungen folgen dem atomaren Registry-Governance-Contract. Materielle Änderungen benötigen Decision, Supersession und Propagation.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
