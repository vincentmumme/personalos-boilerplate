---
schema_version: pos-v1
id: 01a00117-59cb-7293-bfa6-4ef1dfef4011
type: owner-index
title: "System Rules"
created: 2026-04-15
updated: 2026-08-14
index_scope: section
---

# System Rules

## Purpose

Hier liegen atomare bindende systemweite Pflichten, Erlaubnisse und Verbote. Rules besitzen Scope, Trigger, erforderliches Verhalten, Ausnahmegrenze, Verification und Change History. Zusammengesetzte Interface- oder Shape-Verträge gehören nach `system/contracts/`; Defaults nach `system/conventions/`; Betriebsprozeduren nach `system/runbooks/`.

## Ownership and Boundaries

Dieser Index besitzt ausschließlich Navigation. Die verlinkten Rule-Records besitzen ihre jeweilige bindende Semantik; der Index dupliziert weder Regeltext noch Geltungszustand.

## Navigation

- [[system/rules/truth-ownership]] — jede Wahrheit besitzt genau einen kanonischen Owner; andere Orte verlinken oder projizieren.
- [[system/rules/template-governance]] — persistierte POS-Record-Templates liegen unter `system/templates/`; technische Skill-Assets bleiben joblokal.
- [[system/rules/automations/material-run-receipt-retention]] — bindende Hybrid-Retention für Einzelreceipts, technische No-op-Erfassung und Tagesaggregate.
- [[system/rules/core/timezone-and-local-day-boundary]] — ortsbezogene Tageszuordnung, explizite Offsets und hostunabhängige Zeitzonenauflösung.

## Maintenance

Neue Rules werden nur nach ihrer vollständigen Admission ergänzt. Ein Link wird entfernt, wenn der Rule-Record kontrolliert deprecated, ersetzt oder retired wurde; fachliche Änderungen erfolgen niemals im Index.
