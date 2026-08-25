---
schema_version: pos-v1
id: "{{id_rule_truth_ownership}}"
type: rule
title: "Truth Ownership"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Truth Ownership

## Rule

Vor jedem dauerhaften Write wird genau ein kanonischer Owner für die betroffene Wahrheit bestimmt. Das PersonalOS bleibt die persönliche Wahrheitsschicht des Nutzers. Externe oder gemeinsam verwendete Systeme erhalten nur einen ausdrücklich definierten Geltungsbereich und werden im PersonalOS referenziert.

## Scope and Trigger

Die Regel gilt bei Aufnahme, Analyse, Weitergabe, Synchronisation, Migration und Änderung von Kontext sowie bei der Einführung eines neuen externen Wahrheitssystems.

## Required Behavior

- Current Truth genau einem Owner zuordnen und Quellen, Ereignisse, Entscheidungen, Projekte und Views nur verlinken.
- Externe oder gemeinsame Systeme nur für den fachlich festgelegten Bereich als Owner behandeln.
- Persönliche Wahrheit und gemeinsam verantwortete Wahrheit getrennt halten und durch eindeutige Pointer verbinden.
- Feld- oder Objekt-Ownership vor einem Write klären; niemals „last write wins“ als Konfliktregel verwenden.

## Exceptions

Historische Evidenz und auditierbare Ereignisse dürfen denselben Sachverhalt wiedergeben, wenn sie als Quelle statt als aktuelle Wahrheit gekennzeichnet sind. Persönliche Projektionen gemeinsamer Wahrheit sind zulässig, wenn ihr Geltungsbereich und der externe Owner sichtbar bleiben.

## Verification

- Kein Record besitzt fachliche Current Truth, die bereits einem anderen kanonischen Owner gehört.
- Externe Authority ist über Truth-System-, Integration- oder Registry-Pointer nachvollziehbar.
- Synchronisation und Migration erzeugen keinen stillen Dual Write.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
