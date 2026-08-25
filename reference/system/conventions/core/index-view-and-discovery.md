---
schema_version: pos-v1
id: 019ff208-18ce-7a33-9e74-bae8e6d20b50
type: convention
title: "Index, View and Discovery"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Index, View and Discovery

## Convention

Index, View, Table und Tag sind getrennte Auffindbarkeitsfunktionen und niemals konkurrierende Wahrheitsowner. Ein Index ist kuratierte Navigation, eine View ist eine reproduzierbare Projektion kanonischer Records, eine Table ist eine technische Darstellungsform einer View und ein Tag ist optionale bereichsübergreifende Discovery-Metadaten.

## Use When

Diese Convention gilt beim Anlegen oder Pflegen von Folder-Indizes, Entity Home Pages, Dashboards, Obsidian-`.base`-Dateien, Markdown-Tabellen, generierten Übersichten, Tags, Aliases und Knowledge-Graph-Navigation. Fachliche Current Truth, Actions, Decisions, Evidenz und Systemnormen folgen weiterhin ihrem jeweiligen Owner.

## Default

### Index

- Jeder kanonische Root besitzt einen Index. Weitere Ordner erhalten einen Index nur, wenn sie eine eigenständig navigierbare Boundary, einen größeren standardisierten Bereich oder einen erklärungsbedürftigen Einstieg besitzen.
- Reine Jahres-, Monats-, Technik-, Cache- und Leaf-Ordner besitzen standardmäßig keinen Index.
- Ein Index erklärt Zweck, Owner, Abgrenzung, wichtige Unterbereiche, kanonische Einstiege und den nächsten Navigationsschritt.
- Ein Index enthält keine vollständige manuell gepflegte Kinddatei-Liste, keine Taskliste, keinen Runtime-Status und keine fachliche Current Truth.
- Eine Entity Home Page oder ein Project-Hauptrecord ist der kanonische Record des Objekts und kein Folder-Index, auch wenn er dessen verbundenen Kontext navigierbar macht.

### View und Table

- Eine View wird ausschließlich aus kanonischen Records, typisierten Relations oder deklarierter externer Authority abgeleitet.
- Manuell editierbare Inhalte, die nur in einer View existieren, sind unzulässig.
- Generated Views besitzen eine erkennbare Source-, Generation- und Freshness-Grenze und werden nicht unabhängig von ihrer Quelle korrigiert.
- Eine Markdown-Tabelle ist nur dann eine View, wenn ihre Zellen vollständig reproduzierbar sind; narrative oder fachlich neue Inhalte müssen zum kanonischen Owner.
- Obsidian-`.base`-Dateien sind technische View-Definitionen und keine POS-Wahrheit.
- `tables/` bleibt während des Cutovers eine befristete technische Ausnahme. Dort werden standardmäßig keine neuen Views angelegt; nützliche Bestandsviews werden später beim fachlichen Consumer ersetzt oder bewusst entfernt.
- Abgeleitete Views werden bei einem Move nach den kanonischen Records und Links zuletzt neu gebaut.

### Tags und Aliases

- Tags sind optional und verwenden kontrolliertes `lowercase-kebab-case`.
- Tags dienen nur einer realen thematischen Discovery-Frage, die mehrere Owner oder Record-Familien verbindet.
- Tags ersetzen niemals Primary Profile, Lifecycle, State, Owner, Domain, Pfad oder typisierte Relation.
- Es gibt kein universelles Pflicht-Tagfeld. Ein Discovery-Modul wird erst bei mindestens zwei realen Consumern mit definiertem Query- und Validierungsbedarf zugelassen.
- Bestehende Legacy-Tags bleiben bis zur jeweiligen Migrationswelle lesbar und werden nicht automatisch in den Zielvertrag übernommen.
- Aliases dienen echten alternativen Namen, Schreibweisen oder etablierten Begriffen und nicht der Pflege alter Pfade.

## Allowed Variations

- Ein kleiner Ordner darf ohne eigenen Index vollständig vom nächsthöheren Index navigiert werden.
- Ein hochvolumiger Bereich darf einen generierten Inventar-View anbieten, wenn Quelle, Generator und Freshness erkennbar sind.
- Ein Profile darf Tags oder Aliases über ein registriertes Discovery-Modul erlauben, sobald dessen Consumer- und Governance-Schwelle erfüllt ist.
- Eine fachlich verantwortete Summary darf als eigener kanonischer Record existieren; sie ist dann kein bloßer View und benötigt ein eigenes Profile, Sources und Update-Vertrag.

## Examples

- `system/index.md` erklärt Systemowner, Kategorien und Einstiege, ohne alle Systemdateien aufzulisten.
- Eine Project-View darf verknüpfte Actions, Decisions und Interactions anzeigen, schreibt deren State aber nicht fort.
- Eine Übersicht wiederkehrender Ausgaben darf aus kanonischen Finance-Records generiert werden; eine ausschließlich in der Tabelle gepflegte Ausgabe wäre eine zweite Wahrheit.
- `ai-governance` kann ein nützlicher bereichsübergreifender Tag sein. `active`, `project`, `finance` oder `company` duplizieren dagegen strukturierte Felder und sind keine Ziel-Tags.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
