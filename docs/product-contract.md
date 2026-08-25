# Produktvertrag

## Ziel

Dieses Repository liefert eine verständliche, installierbare und erweiterbare Grundlage für ein persönliches Kontextsystem, mit dem unterschiedliche KI-Agenten zuverlässig arbeiten können.

Ein Nutzer kann damit:

1. die Philosophie und die Systemgrenzen verstehen,
2. die aus Vincents real genutztem PersonalOS abgeleitete Systemlogik ansehen,
3. den Kern mit allen oder ausgewählten Modulen aufbauen,
4. einzelne Regeln, Frameworks und Templates übernehmen,
5. das System ohne einen bestimmten Agenten oder Host verwenden.

## Produktgrenzen

Die Boilerplate ist:

- ein strukturierter Ordner als gemeinsame Kontext- und Wahrheitsschicht,
- ein Satz verständlicher Regeln für Ownership, Navigation und Änderungen,
- ein Datenmodell mit wiederverwendbaren Templates,
- ein agenten- und werkzeugneutraler Kern,
- eine modulare Grundlage für spätere Automationen.

Die Boilerplate ist nicht:

- dieselbe betriebsbereite Laufzeit wie Vincents persönliche Instanz,
- ein fertiges Dashboard,
- eine Cloud-Memory-Lösung,
- ein Superagent,
- eine unveränderliche Ordnerstruktur für jedes Leben,
- eine fertige Hermes-, MacMini- oder VPS-Konfiguration,
- ein System, das man verstehen kann, ohne sich mit den eigenen Bedürfnissen zu beschäftigen.

## Unverhandelbare Systemprinzipien

1. **Kontext vor Oberfläche.** Die Dateien bilden das Fundament. Werkzeuge visualisieren oder benutzen sie.
2. **Eine Wahrheit, ein Owner.** Dauerhafte aktuelle Information besitzt genau einen kanonischen Ort.
3. **Input ist noch keine Wahrheit.** Eingang, Arbeitsstand, Entscheidung, aktuelle Wahrheit und Verlauf bleiben unterscheidbar.
4. **Systemlogik ist von persönlichen Daten getrennt.** Regeln und Templates können aktualisiert werden, ohne das Leben des Nutzers zu überschreiben.
5. **Werkzeuge bleiben austauschbar.** Agent, Editor, Host und Suchsystem sind Adapter um das PersonalOS herum.
6. **Verstehen vor Automatisieren.** Erst Daten und Abläufe stabilisieren, dann Automationen ergänzen.
7. **Struktur darf wachsen.** Die Boilerplate gibt sichere Grundlagen vor, aber keine vollständig vorweggenommene Lebensarchitektur.
8. **Private Daten bleiben privat.** Ableitung, Tests und Releases arbeiten nach einem expliziten Ausschluss- und Freigabemodell.

## Produktschichten

### Pflichtkern

Der Kern enthält Bootstrap, Navigation, die elf allgemeinen Root-Bereiche, Systemverträge, Datenmodell, Templates, Mutationsregeln und Prüfungen. Er funktioniert lokal ohne externe Dienste.

### Optionale Module

Module ergänzen optionale Domains und konkrete Fähigkeiten wie Content, Gesundheit, Obsidian, Codex, Claude Code, Hermes, externe Signale, Backups oder Automationen. Kein Modul darf zu einer stillen Voraussetzung des Kerns werden.

### Vollständige Referenz

`reference/` entsteht bei jedem Build aus dem Kern und allen Modul-Payloads. Der Ordner zeigt das vollständige öffentliche System, besitzt aber keine eigenständige Wahrheit.

„Vollständiges öffentliches System“ bezeichnet die portable Systemverfassung und alle bewusst freigegebenen Bestandteile. Es bezeichnet nicht die privaten Laufzeitzustände oder jede instanzgebundene Fachfähigkeit der Referenzinstanz.

### Beispiele

Beispiele zeigen vollständige Abläufe mit erfundenen Personen, Unternehmen, Projekten und Interaktionen. Sie sind Lernmaterial und keine Startwahrheit eines installierten Systems.

## Definition von vollständiger Abdeckung

„100 Prozent Abdeckung“ bedeutet hier:

- Jede versionierte Datei der privaten Referenzinstanz wird vom Exportmodell erkannt.
- Jede Datei ist als Kern, neutralisierte Vorlage, optionales Modul, fiktives Beispiel oder bewusster Ausschluss klassifiziert.
- Wiederverwendbare Systemlogik darf nicht still fehlen.
- Private Daten, lokale Laufzeitzustände und persönliche Konfigurationen dürfen nicht still übernommen werden.
- Neue unklassifizierte Dateien blockieren den Updateprozess.

Es bedeutet ausdrücklich nicht, dass jede private Datei veröffentlicht wird.

## Freigabekriterien für ein öffentliches Release

- vollständige Klassifikation der Referenzinstanz,
- keine erkannten Secrets, privaten Namen oder privaten absoluten Pfade,
- reproduzierbare Generierung ohne unerklärte Unterschiede,
- erfolgreicher Clean-Install-Test in einem leeren Zielordner,
- verständlicher Einstieg ohne Kenntnis der privaten Referenzinstanz,
- menschliche Prüfung aller neutralisierten und optionalen Inhalte,
- erfolgreicher Secret-Scan über Arbeitsbaum und vollständige Git-Historie,
- verständlicher Support- und Security-Pfad ohne Offenlegung privater Inhalte,
- MIT-Lizenz im Repository.
