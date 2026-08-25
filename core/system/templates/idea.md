---
schema_version: pos-v1
id: 019ff1d5-b385-74c6-a7e9-358041ec8674
type: template
title: "Template: Idea"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/core/capture-retention-und-promotion]]"]
target_profile_key: idea
---

# Template: Idea

## Template Contract

Normative Instanzvorlage für eine bewusst bewahrte, dauerhaft wertvolle Möglichkeit, die noch kein bestätigtes Commitment und noch kein Project ist.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
lifecycle: <lifecycle>
evidence_refs: <evidence_refs>
---

# <title>

## Current Truth

<current_truth>

## Idea

<idea>

## Why It Matters

<why_it_matters>

## Source Basis

<source_basis>

## Evidence and Assumptions

<evidence_and_assumptions>

## Development

<development>

## Resolution

<resolution>

## Timeline

- **<date>** | Idea Record created.
```

## Usage

- Nur bei ausdrücklichem Keep, erkennbarem Dauerwert oder einem konkreten Review-Trigger anlegen. Ein Review-Trigger ist ein eigener Attention Trigger und kein Idea-Zustand.
- Die Instanz liegt unter `<domain>/ideas/<uuid>.md` in `identity`, `business`, `knowledge`, `finance` oder `health`. Eine bereits existierende Project-spezifische Idee liegt unter `projects/<project>/working/ideas/<uuid>.md`.
- Content-Ideen verwenden ausschließlich ContentOS. `inbox/`, `notes/`, `operations/`, `people/`, `companies/`, `interactions/`, `daily/`, `automations/` und `system/` sind keine Idea-Owner.
- `active` bedeutet bewusste Entwicklung ohne Commitment. `parked` bedeutet dauerhafte Bewahrung ohne implizite Wiedervorlage. `terminal` benötigt `idea_outcome`; `promoted` verweist mit `promotion_ref` auf den neuen Owner, `merged` mit `merge_target_ref` auf die verbleibende Idea und `rejected` mit `rejection_evidence_refs` auf die tragende Evidenz.
- `active` und `parked` dürfen keine terminalen Outcome- oder Auflösungsfelder tragen. Auch ein terminaler Record darf nur die Relation seines tatsächlichen Outcomes verwenden.
- Promotion verweist nur auf zugelassene neue Ownerprofile; Merge nur auf eine andere Idea. Selbstreferenzen sind in beiden Fällen verboten.
- Eine mögliche spätere Initiative bleibt beim fachlichen Domain-Owner, bis die Project-Eintrittsschwelle erfüllt ist. Ein noch nicht existierendes Project darf nicht nur für die Ablage der Idee erzeugt werden.
- Bei Promotion, Merge oder Rejection bleibt der terminale Idea Record als knapper Provenance-Pointer erhalten; die neue Current Truth liegt beim Zielowner.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
