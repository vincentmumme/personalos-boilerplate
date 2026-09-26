# Starte hier

Dein PersonalOS ist ein Ordner, in dem du und deine KI-Agenten persönlichen Kontext, Projekte, Entscheidungen und Aufgaben nachvollziehbar pflegen. Diese Boilerplate liefert die Struktur und Arbeitsweise dafür. Du füllst sie mit deinem eigenen Leben.

## Ein Satz reicht

Gib deinem Agenten den Link oder öffne den heruntergeladenen Ordner:

```text
https://github.com/vincentmumme/personalos-boilerplate

Ich möchte mit PersonalOS starten.
```

Der Agent liest die Einstiegshilfe, klärt dein Ziel und führt dich durch die nächsten Schritte. Du brauchst vorab weder eine Liste aller Projekte noch Kenntnisse der Ordnerstruktur. Wenn du schon weißt, was du möchtest, sage es direkt, etwa: „Verbessere mein bestehendes PersonalOS“ oder „Erkläre mir erst das System, ohne etwas zu verändern“.

Kann dein Agent keine Webseiten öffnen, lade auf GitHub über **Code → Download ZIP** das Repository herunter, entpacke es und öffne den Ordner im Agenten. Kann er auch keine lokalen Dateien bearbeiten, kannst du mit ihm die Architektur verstehen und den Aufbau vorbereiten. Für die Installation brauchst du anschließend eine Umgebung mit Dateizugriff und Terminal oder führst die Schritte selbst aus.

## Welcher Weg passt zu dir?

| Dein Ziel | Was dabei herauskommt |
| --- | --- |
| **Klein neu starten** | Der Kern mit deinem bestätigten Kontext, optionalen passenden Modulen und einem ersten nutzbaren Arbeitsablauf. Unsere Empfehlung, wenn du noch kein System hast. |
| **Bestehendes verbessern** | Erst eine Bestandsaufnahme, dann eine begrenzte Verbesserung mit Sicherung, nachvollziehbaren Änderungen und Erhalt deines Kontextes. |
| **Verstehen** | Eine verständliche Systemkarte und ein Beispiel vom Eingang bis zum nächsten Schritt. Keine Installation, keine Dateiänderungen. |
| **Vollständig aufbauen** | Der Kern und alle öffentlichen Module. Gemeinsam klärt ihr, was du sofort nutzt und was später eingerichtet wird. |

„Vollständig“ meint die öffentlich portable Architektur aus Vincents PersonalOS: Struktur, Regeln, Templates und Arbeitsweisen. Seine privaten Daten, Accounts, Geräte und laufenden Dienste sind nicht enthalten. Ein installiertes Modul aktiviert noch keinen Dienst.

## So läuft das Onboarding

1. **Orientieren:** Was willst du zuerst erreichen, was existiert bereits und worauf hat dein Agent Zugriff?
2. **Vorbereiten:** Gerät, Werkzeuge, privater Zielordner und vorhandene Dateien prüfen. Kosten oder externe Verbindungen kommen nur ins Spiel, wenn du sie brauchst.
3. **Dich kennenlernen:** Wenige passende Fragen zu dir, deinem Alltag und deiner Zusammenarbeit mit KI. „Später“, „weiß ich noch nicht“ und ein Pseudonym sind erlaubt.
4. **Aufbauen:** Bestätigte Angaben eintragen, prüfen und zeigen, wo sie liegen. Du kannst jederzeit korrigieren oder pausieren.
5. **Benutzen:** Eine echte kleine Aufgabe bearbeiten. Ein neuer Chat findet den gespeicherten Kontext wieder, ohne dass du alles erneut erklärst.

Deine persönlichen Antworten landen in deinem privaten System. Für eine Pause vereinbart ihr einen privaten Speicherort außerhalb der öffentlichen Boilerplate oder haltet den Fortsetzungstext nur im Chat fest.

## Welche Werkzeuge brauche ich?

Zum Lesen genügt ein Browser oder Texteditor. Für die Installation brauchst du **Python ab 3.11**. Ein Agent mit Dateizugriff und Terminal erleichtert den Aufbau; Obsidian ist eine optionale Oberfläche. Git brauchst du nur zum Klonen oder für eine spätere Git-Sicherung, nicht für eine heruntergeladene ZIP-Datei. Ein Server, zusätzliche Module und verbundene Konten sind keine Voraussetzung.

Die Boilerplate selbst hat keine Lizenzkosten. Dein gewählter KI-Dienst oder später verbundene Anbieter können Kosten verursachen. Lokal gespeicherte Dateien können von einem Cloud-Agenten an dessen Anbieter übertragen werden; lokale Dateien bedeuten nicht automatisch lokale KI-Verarbeitung.

- [Technischer Aufbau für macOS, Linux und Windows](docs/getting-started.md)
- [Module und ihre tatsächlichen Voraussetzungen](docs/modules.md)
- [Die erste Woche, Sicherung und Wiederherstellung](docs/first-week.md)
- [Warum PersonalOS existiert](docs/philosophy.md)
- [Systemkarte](docs/system-map.md) und [Produktgrenzen](docs/product-contract.md)
- [Hilfe bei Problemen](SUPPORT.md)

**Für Agenten:** Der Ablauf mit Fragen, Routen und Abschlusskriterien steht in [onboarding/agent-onboarding.md](onboarding/agent-onboarding.md).
