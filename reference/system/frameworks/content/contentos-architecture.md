---
schema_version: "pos-v1"
id: "01a002b7-e000-7bf2-8b69-53c4063ba27b"
type: "framework"
title: "ContentOS v1 Architecture"
created: "2026-08-02"
updated: "2026-08-21"
lifecycle: "active"
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# ContentOS v1 Architecture

## Purpose

Canonical architecture and mental model for ContentOS inside PersonalOS.

## Model

### Current Truth

ContentOS is an object-and-relationship system represented with Markdown and companion data. Files and folders are durable views of the graph; they are not the conceptual model. Domain contracts and templates own shapes. `contentos` owns conversational execution. Providers own no canonical COS truth.

### Layers

```text
POS Constitution     registry + modules + profiles + global templates + validation
Content Domain       strategy + channels + funnel + formats + series + recipes
Knowledge            curated Content Knowledge Base
Operational Graph    Inputs + Ideas + Sources + Pieces + Publications + Evidence
Capability           contentos as the single conversational entry
Providers            storage + production + publishing + tracking + analytics
```

### Stable Relationships

- Input may create or reference Idea, Source, Piece or Candidate.
- Idea may become a Piece only after selection.
- Source may support several Ideas, Research Packs and Pieces.
- Piece may derive from another Piece and owns Context, Spec, Assets and Versions.
- Version belongs to exactly one Piece and packages it for a platform/account.
- Publication belongs to one approved Version and represents one real upload.
- Evidence references the exact Publication, Version, Variant, placement or channel it observed.
- Candidate references its Evidence and targets exactly one durable owner.

### Progressive Materialization

`piece.md` always exists. `context.md`, `production.md` and `assets.md` become first-class companion records when their concerns need independent revisions. Versions, Publications and Analytics live in subfolders. Small variants, observations and hypotheses begin in body or companion data and materialize only when they gain an independent lifecycle.

### Modulares Datenfundament

ContentOS trennt drei Verantwortungen strikt voneinander:

1. Publication Discovery hält das Veröffentlichungsinventar über modulare Plattform- und Kanaladapter vollständig und dedupliziert.
2. Signal Collection sammelt Rohsignale wie Metrik-Snapshots, Kommentare, Antworten und spätere authentifizierte Platform Insights mit signalabhängigen Zeitplänen.
3. Performance Analysis interpretiert ausschließlich bereits gesammelte und nachvollziehbar referenzierte Daten; sie besitzt keinen direkten Plattformabruf.

Jede Schicht kann unabhängig erweitert, anders getaktet und mit einem anderen Provider betrieben werden. Das ContentOS besitzt die stabilen IDs, Beziehungen, Manifeste und normalisierte Evidence. Hochvolumige Rohdaten dürfen in austauschbaren Spreadsheets, Datenbanken oder Datenspeichern liegen, bleiben aber über stabile Pointer, Collection-Metadaten und Coverage im ContentOS nachvollziehbar. Kein konkretes Storage- oder Analytics-Produkt wird dadurch zur kanonischen Content-Wahrheit.

### Productization Boundary

The core contains no instance-specific assumptions. {{user_name}}, {{organization_slug}}, German channel copy, accounts, offers, credentials and providers are instance configuration. This keeps ContentOS demonstrable and distributable without prematurely deciding packaging, pricing or multi-tenancy.

### Canonical Contracts

- [[system/contracts/content/object-model]]
- [[system/contracts/content/workflows]]
- [[system/contracts/content/storage-model]]
- [[system/contracts/content/capability-model]]

### Cutover Boundary

The native POS-v1 cutover was applied on 2026-08-15. All active Content records use admitted Content Primary Profiles, UUIDv7 identities and typed wikilinks. Pre-v1 architecture, old Pieces and retired skills remain only in explicitly labeled Project evidence. There is no compatibility writer, dual-write route or second active schema truth.

### Timeline

- **2026-08-15** - Completed the native POS-v1 admission and atomic Content domain cutover.
- **2026-08-02** - Replaced the Piece-folder-first Legacy architecture with the portable Content graph and contract-owned v1 model.

## Components

Primary profiles, central contracts and templates, Content Knowledge Base, production records and learning evidence.

## Decision Logic

Domain truth stays under `/content`; reusable knowledge stays in the Content KB; general norms stay under `/system`. Datenerhebung wird vor Interpretation aufgebaut: Ohne vollständiges Publication-Inventar und nachvollziehbare Collection Coverage entstehen keine belastbaren Performance-Learnings.

## Interfaces

The `contentos` skill is the single conversational entry and the POS registry is the shape authority.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
