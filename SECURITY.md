# Sicherheit

## Unterstützte Version

Sicherheitskorrekturen werden zunächst für den aktuellen Stand von `main` und die neueste veröffentlichte Version betrachtet. Für ältere Versionen besteht keine garantierte Wartung.

## Sicherheitsproblem vertraulich melden

Veröffentliche vermutete Secrets, private Daten, Pfad-Leaks oder ausnutzbare Schwachstellen nicht in einem öffentlichen Issue oder im Discord.

Nutze auf GitHub unter **Security → Report a vulnerability** die private Sicherheitsmeldung. Teile nur die Informationen, die für Reproduktion und Bewertung notwendig sind, und entferne echte Zugangsdaten aus Screenshots und Beispielen.

Es gibt keine garantierte Reaktionszeit. Bestätigte Leaks werden jedoch vor normalen Feature-Anfragen priorisiert.

## Schutzgrenzen

- Der öffentliche Build darf keine persönlichen oder kundenspezifischen Daten enthalten.
- Installationen schreiben nur in einen leeren oder noch nicht vorhandenen Zielordner.
- Der Manifest-Audit erkennt veränderte Build-Dateien.
- Der Secret-Scan prüft den aktuellen Arbeitsbaum und auf Release-Ebene die vollständige Git-Historie, ohne gefundene Werte auszugeben.
- Nutzer bleiben verantwortlich für die Prüfung eigener Forks, Module, Connectoren und Zugangskonfigurationen.
