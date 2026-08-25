---
schema_version: pos-v1
id: 019ffbfb-532b-7d85-bf20-bca7acb597e4
type: principle
title: "Eine Wahrheit, ein kanonischer Owner"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Eine Wahrheit, ein kanonischer Owner

## Principle

Jede aktuelle Wahrheit besitzt in ihrem Geltungsbereich genau einen kanonischen Owner. Andere Records, Systeme, Views und Skills verlinken, projizieren oder belegen diese Wahrheit, besitzen sie aber nicht erneut.

## Rationale

Mehrere aktive Wahrheitsorte erzeugen Drift, unklare Schreibrechte und widersprüchliche Agentenantworten. Ein eindeutiger Owner macht Propagation, Freshness, Änderung und Recovery überprüfbar.

## Implications

- Jede Information wird nach Semantik und Geltungsbereich geroutet, nicht nach dem Tool, das sie erzeugte.
- Interactions und Sources belegen; Automations verarbeiten; Projects erarbeiten; Domains und Entities besitzen akzeptierte Current Truth.
- Indizes, Tabellen, Dossiers, Briefings und Agentenantworten sind abgeleitete Sichten.
- Ein Systemwechsel benötigt einen bewussten Authority-Cutover oder Pointer, niemals stillen Dual Write.

## Boundaries

Historische Quellen, Events und Decisions dürfen dieselbe Entwicklung aus unterschiedlichen Perspektiven belegen. Das ist keine doppelte Current Truth. Persönliche und gemeinsam verbindliche Wahrheit können unterschiedliche Owner besitzen, wenn ihr Geltungsbereich explizit getrennt ist.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
