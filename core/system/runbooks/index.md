---
schema_version: pos-v1
id: "{{id_runbooks_index}}"
type: owner-index
title: "Runbooks"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: section
---

# Runbooks

## Purpose

Runbooks beschreiben sichere, wiederholbare Abläufe für Änderungen am PersonalOS.

## Ownership and Boundaries

Runbooks operationalisieren Systemverträge. Sie besitzen weder persönliche Wahrheit noch die fachliche Entscheidung eines Skills.

## Navigation

- [[system/runbooks/core/personalos-mutation]] – Dateien kontrolliert ändern und prüfen
- [[system/runbooks/core/test-before-bulk]] – größere Änderungen zuerst an einem kleinen Beispiel beweisen
- [[system/runbooks/modules/index]] – tatsächlich installierte optionale Bereiche und Adapter

Host-, Runtime-, Provider- und Automations-Runbooks werden nur mit dem jeweiligen optionalen Modul installiert und im Modulindex sichtbar gemacht.

## Maintenance

Ein Runbook wird geändert, wenn der sichere Ablauf materiell wechselt. Einmalige Run-Historie gehört nicht in diesen Index.
