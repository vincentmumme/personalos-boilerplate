---
schema_version: pos-v1
id: 019fec87-ac63-7cd5-9c65-e8c32b0bd810
type: contract
title: "System Artifact Ownership and Capability Boundary"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.3.0
---

# System Artifact Ownership and Capability Boundary

## Contract

Normative Systemartefakte werden zuerst nach ihrer Systemkategorie und danach nach ihrem fachlichen Geltungsbereich geordnet. Skills besitzen ausführbare Capabilities, aber weder die verbindliche Form persistierter PersonalOS-Records noch allgemeine POS-Semantik. Jedes persistierte POS-Record-Template besitzt einen kanonischen Owner unter `system/templates/` und ein registriertes Zielprofil.

## Scope

Der Vertrag gilt für Principles, Rules, Contracts, Conventions, Frameworks, Templates, Runbooks, Checks, Data-Model-Artefakte, Skills, skilllokale References und Assets sowie alle von Skills erzeugten PersonalOS-Dateien. Er gilt auch für neue Skills und Domains, deren konkrete Profile erst später zugelassen werden.

## Invariants

- Die physische Grundgrammatik lautet `system/<kategorie>/<scope>/<optionale-objektfamilie>/<artefakt>`.
- `kategorie` bezeichnet den normativen Artefakttyp; `scope` bezeichnet `core`, `system` oder einen kanonischen fachlichen Owner wie `projects`, `interactions`, `content`, `finance` oder `health`.
- Eine Objektfamilie wird nur ergänzt, wenn der Scope mehrere semantisch verschiedene Familien besitzt; sie wird nicht nach Skill, Agent, Provider, Kunde oder Project benannt.
- Persistierte POS-Record-Templates liegen unabhängig von der Zahl ihrer Consumer unter `system/templates/`.
- Skills dürfen lokale Scripts, Provider-Adapter, Prompts, Testdaten und Ausführungsreferenzen halten, solange diese keine normative POS-Record-Form oder allgemeine Semantik definieren.
- Jeder Skill besitzt genau eine kanonische `SKILL.md`. POS-Integration ist eine optionale Schnittstelle innerhalb dieser Datei und begründet weder `CAPABILITY.md` noch einen zweiten zentralen Skillrecord.
- Der Skill-Runtime-Kern bleibt auf Top Level; POS-Foundation und optionale POS-Schnittstellen liegen als geschlossene `pos_*`-Namespace unter `metadata` derselben Datei.
- Skills ohne POS-Integration bleiben gültig, ohne künstliche `system_refs`, Record-I/O-, Template- oder Check-Referenzen anzulegen.
- Ein Verifier darf eine bestehende Norm erzwingen, aber Frontmatter, Pfade, Sections, Enums oder Ownership nicht ausschließlich aus skilllokalen Beispielen ableiten.
- Zusammengehöriger Scope-Kontext wird über direkte `system_refs` und abgeleitete Ansichten erschlossen; ein gemischtes Themenpaket wird nicht zum zweiten Normowner.
- Ein Primary Profile besitzt genau ein kanonisches Creation Template. Materiell verschiedene Shapes benötigen ein eigenes Profile; bloße Varianten werden parametrisiert.

## Interfaces

```text
INDEX -> Skill Resolver -> Owning Skill
                            |
                            +-> direkte system_refs
                            +-> reads_profile_keys / writes_profile_keys
                            +-> template_refs
                            +-> invokes_skill_refs
                            +-> check_refs
```

[[system/contracts/core/capability-interface]] definiert die Semantik und Conditional Rules dieser maschinenlesbaren Schnittstellen. `system_refs` bleibt dadurch ausschließlich normativen Abhängigkeiten vorbehalten.

`interactions` enthält mindestens zwei getrennte Objektfamilien. `meetings` sind zeitlich abgegrenzte Interaktionsereignisse mit Teilnehmern und Zeitpunkt; Call, Telefonat, Videocall und persönliches Treffen sind Kanäle oder Klassifikationen. `conversations` sind fortlaufende oder asynchrone Nachrichtenverläufe; Gmail, WhatsApp und Discord sind Provider oder Quellen und erzeugen nur bei echter semantischer Differenz eigene Profile.

## Compliance

Neue oder migrierte Skills deklarieren direkte Systemabhängigkeiten nur, wenn sie solche besitzen. Für jede von ihnen persistierte POS-Datei müssen vor dem Write Zielprofil, Template und relevante Checks registriert sein. Fehlt ein Vertrag, Profile oder Template, wird zuerst ein vollständiges Admission-Paket geschaffen; ein Skill darf die Lücke nicht durch eine lokale Reference, ein eingebettetes fenced Template oder Validator-Hardcoding schließen.

Bestehende lokale Templates werden nach Funktion inventarisiert. Record-Templates und normative Semantik werden nach `system/` migriert; rein technische Ausführungsassets bleiben beim Skill. Alte Pfade bleiben nur bis zum grünen Consumer-Cutover lesbar und werden danach retired oder durch kontrollierte Redirects ersetzt.

## Evolution

Neue Scopes müssen einem kanonischen POS-Owner entsprechen. Neue Objektfamilien benötigen eine semantische Grenze, die nicht durch Profile, Klassifikation oder Parameter ausdrückbar ist. Weitere Capability-Felder werden nur zugelassen, wenn sie nicht aus dem `capability-io`-Modul ableitbar sind und eine stabile POS-semantische Schnittstelle beschreiben.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
