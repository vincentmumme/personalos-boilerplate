---
schema_version: pos-v1
id: 019ffc1a-c4f9-7777-9e68-a0d61c2990e5
type: contract
title: "Knowledge Topic Wiki Boundary"
created: 2026-08-13
updated: 2026-08-19
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 2.1.0
---

# Knowledge Topic Wiki Boundary

## Contract

`knowledge/` ist der Root für wiederverwendbares, quellengebundenes Wissen, nicht für operative Wahrheit über Personen, Companies, Projects oder Actions. Jedes Topic Wiki besitzt genau einen Topic-Owner, trennt Rohquellen, kompilierte Artikel, Inventar, Datensätze, Quality State und Lifecycle und wird ausschließlich durch die owning Knowledge-Skills verändert.

## Scope

Der Vertrag gilt für Topic-Wikis, Raw Sources, kompilierte Knowledge-Artikel, Inventare, externe Datensätze, Archive, Quality-/Librarian-State und die Hub-Registry. NotebookLM und andere Researchsysteme bleiben Tools oder externe Wissensflächen, nicht automatisch kanonische Knowledge-Owner.

## Invariants

- Source-Ingest und Knowledge-Truth sind getrennt.
- Operative Wahrheit bleibt bei People, Companies, Projects, Business, Finance, Health, Content oder Operations.
- Ein Topic besitzt einen stabilen Slug, genau einen `knowledge-topic` Hauptrecord und einen expliziten Lifecycle.
- Raw Evidence bleibt nachvollziehbar; kompilierte Artikel referenzieren ihre Quellen.
- `index.md`, Section Indexes und `wikis.json` sind abgeleitete Navigation, keine zweite Artikel- oder Registry-Wahrheit.
- Große, mutable oder externe Korpora werden als Dataset-Pointer geführt und nicht in Git kopiert.
- Lazy Module werden erst beim ersten echten Bedarf erzeugt; leere Standardordner sind verboten.
- Archive ist `lifecycle: archived` am Topic Record; archivierte Topics bleiben im normalen Topic-Namespace.
- Persistierte Knowledge Records verwenden ausschließlich die registrierten Profile `knowledge-topic`, `knowledge-source`, `knowledge-article`, `knowledge-inventory-item`, `knowledge-dataset`, `knowledge-assessment`, `knowledge-log` und `owner-index`.
- Ein fremddomainiger ContentOS Candidate im Content-Topic bleibt bis zur eigenen ContentOS-Datenmodellwelle beim ContentOS-Owner und darf von Knowledge-Skills weder gelesen noch umgeschrieben werden, außer bei der ausdrücklich freigegebenen Promotion.

## Interfaces

`knowledge-wiki` besitzt Topic-Scaffolding und die generierte Registry, `knowledge-ingest` Knowledge Sources, `knowledge-compile` Knowledge Articles, `knowledge-inventory` Knowledge-Kandidaten, `knowledge-dataset` externe Korpora, `knowledge-lint` und `knowledge-librarian` Assessments und `knowledge-archive` den expliziten Lifecycle-Wechsel am Topic Record. Skills verwenden die Profile und Templates unter `system/`; Dual Writes oder skill-eigene Record-Schemas sind verboten.

## Compliance

Vor einem neuen Topic werden Scope, vorhandener Owner und Wiederverwendungswert geprüft. Jeder Write behält Provenance und durchläuft owning Skill sowie write-scoped Verification. Breite Reorganisationen benötigen vollständiges Inventar, Consumerplan, repräsentativen Test und Recovery-Beleg.

## Evolution

Die Profile und Capability-I/O sind zugelassen und der Bestands-Cutover ist abgeschlossen. Künftige Erweiterungen erfolgen über die vorhandenen Knowledge-Profile und owning Skills. Ein neuer Recordtyp benötigt nur dann ein neues Profil, wenn Owner, Lifecycle, Relations oder Body Shape materiell abweichen; ein neuer Provider oder ein neues Topic allein reicht nicht aus.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
