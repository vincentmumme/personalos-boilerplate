---
schema_version: pos-v1
id: "{{id_people_index}}"
type: owner-index
title: "People"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: root
---

# People

## Purpose

Kanonischer Einstieg in externe Personen und Beziehungskontext. Pro Person existiert genau ein lesbarer Hauptrecord unter `people/<slug>.md`.

## Ownership and Boundaries

Die eigene Person bleibt unter [[identity/me]]. Projects, Interactions und Actions werden nicht in Personenrecords dupliziert.

## Navigation

Personen werden über ihren lesbaren Slug gefunden und nur bei stabilem Bedarf zusätzlich verlinkt.

## Maintenance

Dieser Index enthält keine automatisch erzeugte Kontaktliste und keine sensiblen Vollprofile fremder Personen.
