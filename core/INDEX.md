---
schema_version: pos-v1
id: "{{id_root_index}}"
type: root-index
title: "PersonalOS Index"
created: "{{install_date}}"
updated: "{{install_date}}"
---

# PersonalOS Index

Dieses PersonalOS ist die Markdown-basierte Kontext- und Wahrheitsschicht von {{user_name}}. Dauerhaft relevante Information besitzt genau einen kanonischen Owner oder einen nachvollziehbaren Pointer auf ein externes Wahrheitssystem.

## Zentrale Einstiege

- [[USER]] – kompakter Startkontext
- [[SOUL]] – gemeinsame Agentenbasis
- [[skills/RESOLVER]] – Fähigkeiten und Routing
- [[system/index]] – Regeln, Verträge, Datenmodell und Systemlogik
- [[operations/index]] – aktuelle Actions und Aufmerksamkeit
- [[projects/index]] – bewusst verfolgte Vorhaben

## Root-Owner

| Root | Verantwortung |
|---|---|
| `inbox/` | ungeklärter, erhaltenswerter Input bis zur Verarbeitung |
| `identity/` | dauerhafte Wahrheit über die eigene Person |
| `people/` | Menschen und Beziehungskontext |
| `companies/` | Organisationen und Unternehmen |
| `projects/` | koordinierte Veränderungsarbeit |
| `interactions/` | Gespräche, Begegnungen und äußere Signale |
| `knowledge/` | dauerhaftes, quellengebundenes Wissen |
| `operations/` | aktuelle Actions, Blocker und Attention Trigger |
| `decisions/` | Belege bestätigter Entscheidungen |
| `daily/` | Tageskontext und Journal |
| `skills/` | ausführbare Fähigkeiten |
| `system/` | Regeln, Datenmodell und Systemmetaebene |

`automations/` wird erst ergänzt, wenn konkrete, stabile Abläufe automatisiert werden. `tables/` kann als technische View-Fläche dienen, besitzt aber keine eigene fachliche Wahrheit.

Optionale Module ergänzen bei Bedarf `business/`, `content/`, `finance/` und `health/`. Agenten, Editoren, externe Signale, Automationen und weitere Hosts bleiben ebenfalls Erweiterungen um dieses Fundament.

## Routing

- Neue, noch ungeklärte Informationen beginnen unter [[inbox/index]].
- Dauerhafte Wahrheit wird zum fachlichen Root und dessen kanonischem Owner propagiert.
- Konkrete nächste Handlungen liegen ausschließlich unter [[operations/index]].
- Größere, bewusst verfolgte Veränderungen werden unter [[projects/index]] koordiniert.
- Ausführbare Abläufe werden über [[skills/RESOLVER]] gewählt.
- Allgemeine Regeln und Systemlogik werden unter [[system/index]] gepflegt.

## Grundgrenzen

- Eine aktuelle Wahrheit besitzt genau einen kanonischen Owner.
- Input, Working Truth, Decision Evidence und Current Truth bleiben unterscheidbar.
- Projects erarbeiten Veränderungen; Domains und Entities besitzen die resultierende Wahrheit.
- Skills führen aus; `/system` besitzt die allgemeinen Regeln.
- Neue Root-Ordner, Profile und Systemkategorien benötigen eine bewusste Entscheidung.

## Pflege

Dieser Index enthält nur die aktive Systemkarte und stabile Navigation. Datei-Inventare, aktuelle Projektstände, Actions und ausführliche Fachwahrheit bleiben bei ihren jeweiligen Ownern.
