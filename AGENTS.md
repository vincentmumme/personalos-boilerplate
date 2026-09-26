# PersonalOS Boilerplate

Du arbeitest in der öffentlichen PersonalOS-Boilerplate. Das private Referenzsystem ist eine Quelle für Maintainer, aber nie ein Ziel für Veröffentlichungen oder Nutzerinstallationen.

## Einstieg mit einem Nutzer

Wenn dir jemand den Repository-Link oder diesen Ordner gibt und mit PersonalOS starten möchte, lies `START-HERE.md` und `onboarding/agent-onboarding.md`. Es gibt vier Wege:

1. klein neu starten und passende Module auswählen
2. ein bestehendes PersonalOS gezielt verbessern
3. Architektur und Arbeitsweise nur verstehen
4. die vollständige öffentlich portable Architektur aufbauen

Leite einen klaren Weg aus dem Auftrag ab. Frage bereits beantwortete Dinge nicht erneut und verlange keine zusätzliche pauschale Planfreigabe für beauftragte Arbeit. Bei unklarem Ziel stelle eine kurze Auswahlfrage mit Empfehlung. Vor Änderungen müssen Zielordner, Umfang und Umgang mit vorhandenem Inhalt geklärt sein. Der Erklärweg bleibt vollständig lesend, einschließlich Gesprächsnotizen.

Prüfe erst Quellzugriff, Umgebung und vorhandenen Kontext. Kannst du den Link oder lokale Dateien nicht lesen, sage das konkret und führe zum nächsten ausführbaren Schritt. Behaupte nie, ungelesene Dateien geprüft, Accounts verbunden oder Dienste gestartet zu haben.

Persönliche Antworten und Installationswerte gehören niemals in diesen öffentlichen Checkout. Halte einen Zwischenstand nur an einem vereinbarten privaten Ort außerhalb des Checkout fest; ohne solchen Ort bleibt er im Chat. Nutze `onboarding/session-template.md`. Nach der Einrichtung gelten die bestehenden registrierten Profile, keine neue Onboarding-Datenstruktur.

Verwende danach nur die Dokumentation, die für die Frage nötig ist:

- Herkunft, Ziele und Grundhaltung: `docs/philosophy.md`
- vollständiger Aufbau und Navigation: `docs/system-map.md`
- externe Systeme, Daten und mehrere Geräte: `docs/external-systems-and-sync.md`
- Produktversprechen und Grenzen: `docs/product-contract.md`
- nachweisbare Abdeckung: `docs/coverage.md`

Lade nicht vorsorglich das gesamte Repository in den Kontext. Nutze `docs/system-map.md`, um die kleinste passende Regel, das passende Framework, Template oder Runbook zu finden.

Beim Aufbau frage adaptiv, üblicherweise eine bis drei zusammenhängende Fragen. Übernimm bekannte Antworten, erlaube Überspringen und markiere Unbekanntes. `onboarding/intake.md` enthält die bedarfsweise Fragenhilfe. Beginne mit einem echten kleinen Nutzen und vertiefe später. Erfinde keine Personen, Werte, Projekte oder Zusagen; fiktive Beispiele bleiben Lernmaterial.

Der Aufbau endet mit einem geprüften ersten Arbeitsablauf, einer inhaltlichen Prüfung samt nötigen Korrekturen und einem neuen Chat, der den Kontext aus Dateien wiederfindet. Bis zum tatsächlichen Test bleibt diese Übergabe offen. Installation, Personalisierung, verbundene Dienste und laufende Automationen sind getrennte Zustände. Technischer Einstieg: `docs/getting-started.md`; Alltag und Wiederherstellung: `docs/first-week.md`.

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

Schreibe in klarem Deutsch. Erkläre nötige Fachbegriffe beim ersten Auftreten und verwende das Glossar unter `core/system/frameworks/core/glossar.md` beziehungsweise `system/frameworks/core/glossar.md` in der installierten Instanz. Technische Ordner, Felder und Typen dürfen Englisch bleiben.
