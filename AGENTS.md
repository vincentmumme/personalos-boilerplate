# PersonalOS Boilerplate

Du arbeitest in der öffentlichen PersonalOS-Boilerplate. Das private Referenzsystem ist eine Quelle für Maintainer, aber nie ein Ziel für Veröffentlichungen oder Nutzerinstallationen.

## Einstieg mit einem Nutzer

Wenn dir ein Nutzer nur den Link zu diesem Repository gibt, lies zuerst `START-HERE.md` und `onboarding/agent-onboarding.md`. Zeige danach diese vier Wege:

1. das vollständige PersonalOS aufbauen
2. den Kern aufbauen und passende Module auswählen
3. Architektur und Arbeitsweise verstehen, ohne Dateien anzulegen
4. einzelne Regeln, Frameworks oder Templates übernehmen

Schreibe keine Datei, bevor der Nutzer einen Weg gewählt und deinen kurzen Plan bestätigt hat.

Verwende danach nur die Dokumentation, die für die Frage nötig ist:

- Herkunft, Ziele und Grundhaltung: `docs/philosophy.md`
- vollständiger Aufbau und Navigation: `docs/system-map.md`
- externe Systeme, Daten und mehrere Geräte: `docs/external-systems-and-sync.md`
- Produktversprechen und Grenzen: `docs/product-contract.md`
- nachweisbare Abdeckung: `docs/coverage.md`

Lade nicht vorsorglich das gesamte Repository in den Kontext. Nutze `docs/system-map.md`, um die kleinste passende Regel, das passende Framework, Template oder Runbook zu finden.

Beim Aufbau fragst du in Blöcken mit drei bis fünf Fragen. Fasse jede Antwortgruppe zusammen. Beende das Interview, sobald ein brauchbarer Startkontext vorliegt. Erfinde keine Personen, Projekte oder andere persönliche Records. Beispiele bleiben unter `examples/`.

Wenn mehrere Geräte beteiligt sind, richte pro PersonalOS-Repository genau einen automatischen Git-Writer ein. Lies vor jeder Einrichtung `docs/external-systems-and-sync.md` und die Module `multi-host` sowie `backup-git`.

## Verbindliche Grenzen

- `core/` enthält das Pflichtfundament.
- `modules/` enthält optionale Bereiche, Werkzeuge und Infrastruktur. Kein Modul ist standardmäßig aktiv.
- `reference/` wird aus `core/` und allen Modul-Payloads erzeugt. Bearbeite es nicht direkt.
- Systemlogik und persönliche Daten bleiben getrennt.
- Regeln, Frameworks, Templates und Checks gehören in den Kern oder ein klar benanntes Modul.
- Secrets, private IDs, absolute private Pfade, Live-Zustände und aktive Automationen dürfen nicht in die Boilerplate.
- Neue Quelldateien brauchen eine ausdrückliche Exportklassifikation.

## Maintainer-Arbeit

- `policy/export-policy.json` klassifiziert die private Referenzinstanz vollständig und fail-closed.
- `blueprints/` enthält öffentliche Ersetzungen und zusätzliche Modultexte.
- Generierte Dateien unter `core/`, `modules/` und `reference/` werden nicht zu drei Wahrheiten. `reference/` bleibt reine Komposition.
- Jeder Sync läuft in einen isolierten Build-Ordner und endet mit Audit, Tests und menschlicher Freigabe.
- Das Repository verteilt noch keine Updates in bereits personalisierte Nutzerinstanzen.

## Sprache

Schreibe in klarem Deutsch. Erkläre nötige Fachbegriffe beim ersten Auftreten und verwende das Glossar unter `system/frameworks/core/glossar.md`. Technische Ordner, Felder und Typen dürfen Englisch bleiben.
