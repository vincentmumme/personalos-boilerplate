---
schema_version: pos-v1
id: "{{id_daily_index}}"
type: owner-index
title: "Daily"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: root
---

# Daily

## Purpose

Einstieg in den zeitlichen Querschnitt aus Day Records, Activity Contributions und optionalen Journal Entries.

## Ownership and Boundaries

Daily zeigt, was an einem Tag geschah. Es ersetzt weder Domain Truth noch Actions, Interactions oder Automation Receipts.

## Navigation

Tageskontext liegt unter `daily/<year>/<date>/` und wird nach Datum gefunden.

## Maintenance

Es werden nur Tage materialisiert, für die tatsächlich relevanter Activity oder Journal Context existiert.
