# Agentengeführtes Onboarding

Diese Anleitung richtet sich an den Coding Agent, der mit dem Nutzer arbeitet.

## 1. Noch nichts schreiben

Lies `START-HERE.md`, `docs/product-contract.md` und `modules/catalog.json`. Nutze `docs/system-map.md` zur Navigation und lies `reference/INDEX.md` nur bei Bedarf. Frage danach, welchen Weg der Nutzer wählen möchte:

1. vollständiges PersonalOS
2. Kern mit ausgewählten Modulen
3. nur verstehen
4. einzelne Teile übernehmen

Erkläre für jeden Weg in einem Satz, welches Ergebnis entsteht. Warte auf die Wahl. Zeige dann einen kurzen Plan und warte auf die Bestätigung.

## 2. Kontext in kleinen Blöcken erfragen

Frage pro Runde drei bis fünf Punkte. Fasse die Antworten zusammen und lasse den Nutzer Fehler korrigieren.

### Person und Ziel

- Wie soll das System die Person nennen?
- Wofür soll das PersonalOS zuerst helfen?
- Welche Probleme treten heute beim Arbeiten mit KI auf?
- Welche Regeln soll jeder Agent beachten?

### Aktuelle Arbeit

- Welche laufenden Projekte brauchen Kontext?
- Welche Menschen und Firmen kommen oft vor?
- Wie hält der Nutzer Entscheidungen und nächste Schritte heute fest?
- Welche bestehenden Ordner oder Werkzeuge soll der Agent berücksichtigen?

### Passende Erweiterungen

- Welche optionalen Lebens- oder Arbeitsbereiche braucht der Nutzer?
- Welche Agenten oder Editoren sollen den Ordner nutzen?
- Gibt es externe Signale, Automationen, Backups oder weitere Hosts?

Wenn externe Systeme oder mehrere Geräte relevant sind, lies `docs/external-systems-and-sync.md`. Plane pro PersonalOS-Repository genau einen automatischen Git-Writer. Ein zweiter Host beginnt lesend und erhält erst nach einem ausdrücklichen Writer-Cutover die Git-Verantwortung.

Beende die Fragen, sobald ein brauchbarer Startkontext vorliegt. Ein PersonalOS wächst mit echter Nutzung.

## 3. Installationsplan zeigen

Der Plan nennt:

- Zielordner
- gewählten Weg
- Kern und ausgewählte Module
- persönliche Records, für die echte Angaben vorliegen
- bestehende Dateien, die unberührt bleiben
- Prüfungen nach der Installation

Lege keine leeren persönlichen Records an, nur um eine Struktur vollständig wirken zu lassen. Root-Ordner und ihre Indexdateien gehören zum Kern.

## 4. Kontrolliert aufbauen

Für einen neuen Zielordner kann der Agent das lokale Werkzeug verwenden:

```bash
pos-boilerplate install \
  --build /path/to/personalos-boilerplate \
  --destination /path/to/new/PersonalOS \
  --values /path/to/install-values.json \
  --all-modules
```

Für eine Auswahl ersetzt der Agent `--all-modules` durch wiederholte Angaben wie `--module content --module codex`.

Bei Weg 3 schreibt der Agent nichts. Bei Weg 4 kopiert er nur die bestätigten Teile und erklärt nötige Abhängigkeiten.

## 5. Ergebnis gemeinsam prüfen

Zeige dem Nutzer:

- den Root-Aufbau
- die Startdateien für Agenten
- die persönlichen Angaben, die aus dem Onboarding entstanden sind
- die gewählten Module
- einen kleinen Ablauf vom Input bis zum kanonischen Owner
- die ausgeführten Prüfungen

Der Nutzer soll verstehen, warum die Struktur existiert und wie er sie verändert.
