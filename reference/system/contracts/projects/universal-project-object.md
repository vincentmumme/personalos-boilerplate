---
schema_version: pos-v1
id: 019ffbfb-6748-7d66-845b-6704932dd5ce
type: contract
title: "Universeller Project Object Contract"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.1.0
---

# Universeller Project Object Contract

## Contract

Ein Project ist die stabile Arbeitsidentität für eine bewusst verfolgte Veränderung, Untersuchung oder ein gewünschtes Ergebnis, das koordinierte Arbeit über mehr als eine einzelne Action erfordert. Deal, Opportunity, Initiative, Migration und Program verwenden denselben Project-Container und unterscheiden sich durch Workflow, fachliche Phase, Lifecycle und Relations.

## Scope

Der Vertrag gilt für private, persönliche, geschäftliche, gemeinsame, externe und systemische Vorhaben. Ein Project entsteht erst, wenn das Vorhaben benennbar, von {{user_name}} bewusst verfolgt und größer als eine einzelne Action ist. Ein Gedanke bleibt Capture oder Idea; eine einzelne Handlung bleibt Action; fortlaufende Current Truth bleibt Domain.

## Invariants

1. Jedes Project besitzt genau einen lesbaren peer-level Namespace `projects/<slug>/` und einen Hauptrecord `projects/<slug>/<slug>.md`.
2. Project-Ordner werden nicht physisch ineinander verschachtelt; Beziehungen laufen über typisierte Relations.
3. Die sechs semantischen Module `context`, `definition`, `planning`, `working`, `deliverables` und `evidence` sind verfügbar und entstehen erst mit dem ersten Artefakt.
4. Der Hauptrecord besitzt Identität, Outcome, Scope, Rollen, Lifecycle, Project Current Truth, Navigation, Propagation und Timeline.
5. Actions, Decisions, Interactions, akzeptierte Domain Truth, Repository-Implementierung, Binärassets, Secrets und Finance bleiben bei ihren eigenen Ownern.
6. Project Working Truth wird erst durch ein belegtes Gate zur Current Truth des zuständigen fachlichen Owners.
7. Ein Wechsel von Deal zu Delivery, Migration zu Betrieb oder internem zu externem Truth System ändert niemals Project-ID, Namespace oder Historie.
8. `lifecycle` beschreibt den universellen Bestandszustand des Projects. `workflow` beschreibt die primäre Arbeitslogik, `project_phase` optional deren aktuellen fachlichen Schritt und `commercial_state` optional das dauerhafte kommerzielle Ergebnis. Keine dieser Achsen ersetzt eine andere.

## Interfaces

- `operations/` besitzt ausführbare Actions und Attention Trigger.
- `decisions/` besitzt kanonische Entscheidungsbelege.
- `interactions/` und Source Records besitzen ursprüngliche Evidenz.
- Domains und Entities besitzen akzeptierte Current Truth.
- Repositories und externe Asset Stores werden über Pointer und Manifest referenziert.
- Der Project-Hauptrecord hält eine abgeleitete Outcome-/Propagation-Sicht und benennt bewusste No-ops.

## Compliance

Das `project`-Profil, das zentrale Project-Template und die `working-note`-Profile prüfen Hauptrecord und Module. Neue Top-Level-Project-Module benötigen eine ausdrückliche Architekturentscheidung. Bestandsmigrationen müssen flache Projects, Deals, Programs, Migrationen, Sync-Konflikte, Consumer, fachliche Phasen und Recovery gemeinsam inventarisieren.

## Evolution

Workflow-spezifische Phasen verwenden zunächst den kontrollierten lower-kebab Wert `project_phase`; wiederkehrende Phasenfamilien können später mit eigenem Enum-Vertrag zugelassen werden. `commercial_state` bleibt auf `open`, `won`, `lost` und `withdrawn` begrenzt. Zusätzliche Module, verschachtelte Project-Namespaces oder getrennte Deal-/Program-Roots sind breaking und benötigen eine neue {{user_name}}-Entscheidung.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
