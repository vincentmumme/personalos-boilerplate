---
schema_version: pos-v1
id: "{{id_companies_index}}"
type: owner-index
title: "Companies"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: root
---

# Companies

## Purpose

Kanonischer Einstieg in Organisationen und Unternehmen. Pro externer Entität existiert genau ein lesbarer Hauptrecord unter `companies/<slug>.md`.

## Ownership and Boundaries

Projects, Interactions, Business-Objekte und Actions bleiben bei ihren eigenen Ownern. Neue Records folgen [[system/templates/entities/company]].

## Navigation

Company Records werden über ihren lesbaren Slug gefunden und nur bei stabilem Bedarf zusätzlich verlinkt.

## Maintenance

Dieser Index enthält keine automatisch erzeugte Liste aller Unternehmen und keine aktuellen Projektstände.
