---
schema_version: pos-v1
id: "{{id_decisions_index}}"
type: owner-index
title: "Decisions"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: root
---

# Decisions

## Purpose

Einstieg in bestätigte Entscheidungen und ihren damaligen Grund.

## Ownership and Boundaries

Decision Records sind semantisch unveränderliche Belege. Die daraus resultierende aktuelle Wahrheit bleibt beim jeweils betroffenen Owner.

## Navigation

Entscheidungen liegen datiert unter `decisions/<year>/` und werden über betroffene Owner verlinkt.

## Maintenance

Eine neue Richtung erzeugt eine neue Entscheidung mit expliziter Nachfolgebeziehung; alte Entscheidungen werden nicht umgeschrieben.
