---
schema_version: pos-v1
id: 019ff208-18a0-7b8e-a010-595ef1746cbb
type: contract
title: "Internal Links and Path Mutations"
created: 2026-08-11
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.1.0
---

# Internal Links and Path Mutations

## Contract

Interne PersonalOS-Verweise bleiben native, pfadqualifizierte Obsidian-Wikilinks. Die UUIDv7 im Zielrecord ist dessen stabile Identität; der Linkpfad ist seine lesbare Navigation. Verschiebungen und Umbenennungen bewahren die UUID, aktualisieren alle kontrollierbaren eingehenden Verweise als Teil derselben Mutation und hinterlassen keine parallele aktuelle Wahrheit.

## Scope

Der Contract gilt für interne Body-Links, typisierte Frontmatter-Relations, Profile-Pfadänderungen, einzelne Moves und Renames, Root- oder Domainmigrationen, Redirects, Backlinks und Linkprüfungen. Externe URLs, externe System-IDs und Asset-Pointer folgen ihrem jeweiligen Authority- oder Pointer-Vertrag.

## Invariants

- Interne Links verwenden `[[voller/vault-relativer/pfad]]` oder `[[voller/vault-relativer/pfad|Lesetext]]`; die Endung `.md` wird weggelassen.
- Relative Markdown-Links innerhalb eines portablen Skill-Pakets dürfen dessen eigene `references/`, `scripts/` oder `assets/` adressieren, weil sie Teil der runtimeübergreifenden `SKILL.md`-Schnittstelle und keine persistierte Graphrelation sind. Persistierte POS-Records, die ein Skill erzeugt oder verändert, bleiben vollständig an den Wikilink-Vertrag gebunden.
- Basename-only-Links sind nur zulässig, wenn ein technischer Einstiegspunkt bewusst root-eindeutig ist und die Linkprüfung ihn deterministisch auflöst. Neue fachliche Relations verwenden immer den pfadqualifizierten Zielpfad.
- Maschinenrelevante Beziehungen stehen in registrierten, typisierten Frontmatter-Feldern mit `_ref` beziehungsweise `_refs`. Assoziative oder narrative Beziehungen dürfen im Body stehen.
- UUIDs werden nicht als eigene sichtbare Linksyntax verwendet. Validator und Migrationsmanifest prüfen Ziel-UUID, Zielprofil und Pfadzuordnung hinter dem Wikilink.
- Inverse Backlinklisten werden abgeleitet und nicht manuell als zweite Relation gepflegt.
- Ein Move oder Rename erzeugt keinen neuen Record: UUID und `created` bleiben unverändert. Ein rein technischer Move verändert `updated` nicht.
- Alle kontrollierbaren eingehenden Links, typisierten Relations, Indizes, Views, Templates, Skills und anderen Consumer werden im selben kontrollierten Slice aktualisiert und anschließend auf kaputte, mehrdeutige und verbliebene Altpfade geprüft.
- Ein Migrationsreceipt hält mindestens UUID, alten Pfad, neuen Pfad, betroffene Consumer, Linkänderungen, verbleibende Ausnahmen und Recovery-Pfad fest.
- Redirects sind temporäre Kontinuitätspointer ohne fachliche Wahrheit. Sie werden nur verwendet, wenn externe oder nicht kontrollierbare Verweise den alten Pfad real benötigen, und besitzen eine explizite Entfernungsvoraussetzung.
- Aliases repräsentieren echte alternative Namen mit Discovery-Wert. Sie werden nicht allein als stiller Ersatz für eine saubere Linkmigration angelegt.

## Interfaces

```text
Path Contract + Target UUID
  -> Inbound-Link- und Consumer-Inventar
  -> Dry Run mit Collision- und Linkplan
  -> atomarer Move/Rename und Linkrewrite
  -> Rebuild abgeleiteter Views
  -> Link-, Profile- und Recovery-Postflight
```

[[system/conventions/core/record-naming-and-temporal-paths]] definiert die Pfadform. [[system/contracts/core/personalos-mutation-contract]] und [[system/runbooks/core/personalos-mutation]] besitzen die allgemeine Mutation Discipline. [[system/checks/core/markdown-record-integrity]] prüft neue kaputte oder mehrdeutige Links; profilgebundene Validatoren prüfen Zielprofile und erlaubte Pfade.

## Compliance

Eine Pfadmutation ist nicht compliant, wenn die UUID wechselt, kontrollierbare eingehende Links ungeplant verbleiben, Basename-Kollisionen nicht aufgelöst sind, eine alte und neue Current Truth parallel aktiv bleiben, ein Redirect ohne realen Kontinuitätsbedarf entsteht oder der Recovery-Pfad fehlt. Obsidian-interne automatische Linkupdates gelten nur dann als Nachweis, wenn der anschließende repositoryweite Link- und Consumer-Postflight grün ist.

## Evolution

Eine spätere technische ID-Auflösung darf als Validator- oder Navigationsebene ergänzt werden, ersetzt aber native Wikilinks nur nach ausdrücklicher Architekturentscheidung und vollständigem Consumer-Cutover. Neue Relationstypen werden über das zentrale Datenmodell aufgenommen; neue Move-Klassen erweitern den Mutation Contract oder ein spezifisches Runbook.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
