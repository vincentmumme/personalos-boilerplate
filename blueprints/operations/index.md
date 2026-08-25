---
schema_version: pos-v1
id: "{{id_operations_index}}"
type: owner-index
title: "Operations"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: root
---

# Operations

## Purpose

Kanonischer Einstieg in aktuelle Actions, Waiting, Blocker, Deferred Items und Attention Trigger.

## Ownership and Boundaries

Operations besitzt Ausführungs- und Aufmerksamkeitswahrheit. Projects, Decisions, Interactions, Systemzustand und fachliche Domain Truth bleiben bei ihren eigenen Ownern.

## Navigation

- Bestätigte Commitments: [[operations/actions/index]]
- Spätere Neubewertung ohne aktuelles Commitment: [[operations/attention-triggers/index]]

## Maintenance

Statuslisten sind abgeleitete Sichten. Jede Action und jeder Attention Trigger bleibt ein atomarer Record.
