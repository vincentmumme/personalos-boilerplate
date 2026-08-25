---
schema_version: pos-v1
id: "{{id_finance_index}}"
type: owner-index
title: "Finance"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: root
---

# Finance

## Purpose

Kanonischer Einstieg in Konten, Belege, Rechnungen, wiederkehrende Verpflichtungen, Kosten, Zeiten und Steuerdossiers.

## Ownership and Boundaries

Finanzdaten sind besonders sensibel. Binäre Belege können extern liegen, müssen aber durch nachvollziehbare Records referenziert bleiben.

## Navigation

Objektfamilien werden erst mit dem ersten echten Finance Record als Unterbereich angelegt.

## Maintenance

Secrets und vollständige Zahlungsdaten gehören nicht in Markdown. Rechtlich autoritative Buchungswahrheit bleibt beim jeweiligen Fachsystem.
