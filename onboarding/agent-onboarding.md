# Agentengeführtes Onboarding

Ziel ist ein passender, verständlicher Start mit überprüfbarem Nutzen. Eine erfolgreiche Installation allein ist noch kein abgeschlossenes Onboarding. Diese Anleitung steuert die Zusammenarbeit; persönliche Angaben gehören in die private Nutzerinstanz.

## 1. Auftrag und Zugriff klären

Lies `START-HERE.md`. Ordne das Anliegen einem der vier Wege zu. „Ich will klein anfangen“ ist bereits eine Auswahl. „Ich möchte mit PersonalOS starten“ lässt noch offen, ob ein System existiert: Frage etwa „Hast du schon einen Ordner mit persönlichem Kontext, den wir weiterentwickeln sollen? Wenn nicht, empfehle ich den kleinen Neustart.“ Stelle kein Pflichtmenü vor jede eindeutige Anfrage.

Übernimm den vorhandenen Gesprächskontext und bestehende Freigaben. Zeige vor Änderungen einen kurzen konkreten Plan mit Ziel, Umfang und nächstem Ergebnis. Für bereits beauftragte, sichere Arbeit brauchst du keine zweite pauschale Bestätigung. Kläre fehlende Entscheidungen, fremde bestehende Inhalte, externe Wirkungen oder kostenpflichtige Schritte, bevor du davon abhängige Aktionen ausführst.

Prüfe den tatsächlichen Zugriff:

- **Nur Repository-Link:** Lies die Einstiegspunkte über verfügbare Web-/Repository-Werkzeuge. Klonen oder ZIP-Entpacken erst für einen Aufbauauftrag und in einen geeigneten Quellordner. Fehlt Zugriff, führe zum ZIP-Download und lokalen Öffnen. Gib an, welche Dateien du noch nicht lesen konntest.
- **Lokaler Ordner:** Prüfe, ob `AGENTS.md`, `START-HERE.md`, `core/`, `modules/catalog.json`, `manifest.json` und `pyproject.toml` zusammen vorhanden sind. Das Quellrepository ist nicht das persönliche Zielsystem.
- **Reiner Chat ohne Dateizugriff:** Erklären und vorbereiten ist möglich; Installation oder Speicherung nicht als erledigt darstellen. Übergib den nächsten konkreten Schritt für eine geeignete Umgebung.
- **Fortsetzung:** Lies einen vom Nutzer angegebenen privaten Zwischenstand. Prüfe Ziel und Dateien erneut; ein alter Check beweist keinen aktuellen Zustand. Frage nur offene oder inzwischen veränderte Punkte.

Lade danach nur die benötigte Vertiefung: Produktgrenzen in `docs/product-contract.md`, Module in `modules/catalog.json` und `docs/modules.md`, Navigation in `docs/system-map.md`. Lies nie vorsorglich alle Referenzdateien oder private Ablagen.

## 2. Technische und persönliche Vorbereitung

Beim Erklärweg entfallen Installation, Tool-Setup, persönliches Interview und gespeicherter Zwischenstand. Für die anderen Wege prüfe die Umgebung lesend und frage nur, was du nicht verlässlich ermitteln kannst:

| Prüfen | Konsequenz |
| --- | --- |
| Betriebssystem, Terminal und Python-Version | Passende Anleitung aus `docs/getting-started.md`; Python mindestens 3.11. Keine PowerShell-Aktivierungsrichtlinie ändern. |
| Agent, Editor und verfügbare Fähigkeiten | Dateizugriff, Terminal und Netz separat feststellen. Ein Chat-Abonnement beweist keinen API-Zugriff. Obsidian und Git sind optional. |
| Bestehender Kontext und gewünschter Zielordner | Nur ausdrücklich zugängliche, aufgabenrelevante Pfade lesen. Neuanlage braucht ein leeres oder nicht vorhandenes Ziel außerhalb des Quellrepository. Ein bereits als Obsidian-Vault geöffneter Ordner, der nur `.obsidian/` und Systemdateien wie `.DS_Store` enthält, zählt als leer; diese Einträge bleiben erhalten. |
| Sprache, Zeitzone und Zeitrahmen | Vorschlag aus Umgebung benennen und bestätigen lassen, wenn er für Termine benötigt wird. Kurzer Einstieg darf ohne vollständige Biografie funktionieren. |
| Speicherung und Datenschutz | Private Dateien nicht in den öffentlichen Checkout, Issue oder Pull Request schreiben. Cloud-KI-Verarbeitung erklären; sensible Quellen nur im gewünschten Umfang nutzen. |
| Accounts, Kosten und Berechtigungen | Für den lokalen Kern keine externen Accounts nötig. Bei einem gewünschten Dienst Zweck, notwendigen Zugriff und mögliche Kosten klären; keine Secrets in Markdown oder Chat anfordern. |
| Vorhandene Sicherung und weitere Geräte | Vor Bestandsänderungen wiederherstellbare Sicherung verlangen oder im beauftragten Umfang anlegen. Sync allein ist keine Sicherung; mehrere Geräte brauchen geklärte Schreibzuständigkeit. |

Nutze den lesenden `doctor` aus `docs/getting-started.md`, sobald das CLI verfügbar ist. Er prüft technische Voraussetzungen, nicht erfolgreiche Account-Anmeldung, Providerpreise, individuelle Datenschutzentscheidungen oder die Wiederherstellbarkeit einer Sicherung. Repariere konkrete Blocker oder erkläre den verbleibenden Schritt. Umgehe sie nicht mit `--skip`-Ideen oder dem Löschen vorhandener Dateien.

## 3. Passende Route ausführen

### A. Klein neu starten

Empfehle den Kern und nur Module mit einem benannten unmittelbaren Nutzen. Nutze `onboarding/intake.md` für einen Namen oder ein Pseudonym, das erste Ziel und hilfreiche Regeln der Zusammenarbeit. Unbekannte Eigenschaften bleiben unbekannt. Drei gute Antworten können für einen Anfang ausreichen.

Stelle den Plan vor: privates Ziel, bestätigter Kontext, Module, erster Arbeitsablauf und Prüfungen. Erzeuge eine private Kopie von `onboarding/install-values.template.json` und trage ausschließlich bestätigte Angaben ein. Die Datei unter `examples/` ist ein fiktives Demo-Profil und kein Ausgangsprofil für echte Menschen.

Installiere nach `docs/getting-started.md`, ohne `--all-modules`, sofern es keinen entsprechenden Wunsch gibt. Danach Bootstrap der erzeugten Instanz lesen und echte Records nach ihren registrierten Profilen anlegen. Erzeuge kein Projekt für jede erwähnte Idee, Rolle oder Dauerverantwortung; nur für tatsächlich gewollte Vorhaben mit einem Ergebnis.

**Erfolg:** Installation und Datenmodellprüfung erfolgreich; bestätigte Angaben auffindbar; ein echter kleiner Ablauf samt inhaltlicher Prüfung abgeschlossen; neuer Chat findet den Kontext; Nutzer kennt nächsten Schritt und Sicherungsweg.

### B. Bestehendes PersonalOS verbessern

Zuerst lesen, nicht installieren. Lade den Bootstrap des bestehenden Systems und respektiere dessen eigene Regeln. Erfasse im vereinbarten Umfang: Einstiegspunkte, aktuelle Owner, persönliche Daten, Templates, Agentenregeln, genutzte Dienste, Sicherung und konkrete Reibung. Übertrage nicht automatisch die gesamte Boilerplate.

Schlage eine kleine Verbesserung mit Begründung, betroffenen Dateien, Abhängigkeiten und Prüfweg vor. Prüfe Links, referenzierte Regeln und nötige Profile gemeinsam; eine einzelne kopierte Vorlage kann ohne ihre Verträge unbrauchbar sein. Zeige Konflikte ausdrücklich. Ein bestehender Auftrag zu einer klar begrenzten Änderung reicht als Autorisierung; unbekannten Umfang oder widersprüchliche Regeln klären.

Sichere betroffene Inhalte mit einem verifizierten Rückweg, dann integriere die passende Änderung. Falls ein Vergleichssystem nötig ist, installiere die Boilerplate separat in ein leeres privates Testziel. Der Installer ist kein Merge- oder Update-Werkzeug und wird nie gegen den bestehenden Inhalt ausgeführt. Zeige anschließend die tatsächlichen Unterschiede und führe die Prüfungen des Zielsystems aus.

**Erfolg:** Mindestens ein vereinbartes Problem gelöst und am realen Ablauf geprüft; Änderungen und Abhängigkeiten nachvollziehbar; bestehender Kontext erhalten; Sicherung und Rückweg benannt; Folgewünsche getrennt festgehalten. Ein kompletter Neuaufbau ist dafür nicht erforderlich.

### C. Verstehen, ohne etwas zu verändern

Erkläre mit einem ausdrücklich fiktiven Beispiel: Nachricht oder Notiz → nachvollziehbare Quelle → zuständiger Kontext → konkrete nächste Handlung. Zeige `INDEX`, `USER`, `SOUL`, fachliche Owner, Templates und Checks nur so weit, wie es die Frage braucht. Trenne Prinzipien von Vincents konkreter Umsetzung und Dokumentation von laufenden Fähigkeiten.

Keine Installation, keine Kopie, kein Tool-Setup, kein gespeicherter Session-Record, keine persönliche Bestandsaufnahme ohne Auftrag. Ein lesender Blick in freigegebene bestehende Dateien ist möglich. Ergebnis und Fortsetzung bleiben im Chat, sofern nicht separat eine Speicherung beauftragt wird.

**Erfolg:** Die Person kann erklären, wo aktuelle Wahrheit liegt, wie ein Agent beginnt und wie eine Änderung geprüft wird. Beantworte ihre Rückfrage anhand eines Beispiels und benenne einen passenden nächsten Weg. Ein Wechsel zum Aufbau braucht einen entsprechenden Auftrag.

### D. Vollständige öffentliche Architektur aufbauen

Erkläre vorab: Kern plus alle öffentlichen Module ergibt den vollständigen portablen Aufbau. Private Daten, private Spezialfähigkeiten, verbundene Konten, Server und aktive Automationen werden nicht mitgeliefert. Lies `docs/product-contract.md`, den Modulkatalog und die für die gewünschten Dienste relevanten Runbooks.

Installiere mit `--all-modules` in ein leeres privates Ziel. Personalisierung und erster Nutzen folgen Route A. Gehe anschließend die Module in Gruppen durch: Lebens-/Arbeitsbereiche, Oberflächen/Agenten und Infrastruktur. Halte für gewünschte Erweiterungen getrennt fest: **Dateien installiert**, **Einrichtung offen**, **Verbindung geprüft**, **tatsächlich im Betrieb geprüft**. Nicht benötigte Dienste bleiben uneingerichtet. Wähle beim ersten Ablauf nur eine überschaubare Fähigkeit.

Bei mehreren Geräten oder Git-Sicherung vor Einrichtung `docs/external-systems-and-sync.md` lesen: genau ein automatischer Git-Writer je PersonalOS. Zugangsdaten über dafür vorgesehene Secret Stores handhaben. Keine Accounts, Abonnements, Zeitpläne oder Veröffentlichungen allein aus der Modulwahl ableiten.

**Erfolg:** Alle öffentlichen Module installiert und geprüft; Systemkarte verständlich; erster eigener Ablauf funktioniert; Einrichtung und Betrieb der gewünschten Dienste einzeln belegt oder offen markiert; private Referenzdaten sind nicht als fehlende „Vollständigkeit“ versprochen.

## 4. Fortschritt und Pausen

Halte Entscheidungen, offene Punkte und den nächsten Schritt während des Gesprächs knapp sichtbar. Niemand muss denselben Fragenblock nach einer Pause erneut beantworten.

Vor der Installation: Verwende bei vereinbartem privaten Speicherort `onboarding/session-template.md` als gewöhnliche Markdown-Arbeitsnotiz **außerhalb** des öffentlichen Quellordners und **außerhalb** des noch leeren Installationsziels. Lege auch Installationswerte dort ab. Gibt es keinen vereinbarten Ort, gib einen kopierbaren Fortsetzungstext im Chat aus. Unnötige Quellenkopien und Secrets gehören nicht in die Notiz. Der Erklärweg bleibt ohne separate Speicheranweisung vollständig lesend.

Nach der Installation: Falls das tatsächliche Einrichtungsvorhaben weiterläuft, verwende ein bestehendes passendes Project oder lege es nach `system/templates/project.md` und dem registrierten `project`-Profil an. Die Fortsetzung kann darin als `working-note` unter `projects/<slug>/working/onboarding.md` liegen, nach dem registrierten Template mit `Working Truth` und `Re-entry`. Kein neuer Record-Typ, kein `onboarding/`-Root im persönlichen System. Ist der Aufbau bereits abgeschlossen und kein solches Vorhaben nötig, erfinde dafür kein Projekt; eine Übergabe im Chat genügt.

Die Arbeitsnotiz verweist auf bestätigte persönliche Owner und dupliziert sie nicht dauerhaft. Schreibe technische Zustände anhand von Ergebnissen, nicht Absichten. Ein späterer Agent verifiziert sie erneut, bevor er davon abhängige Änderungen ausführt.

## 5. Ersten Nutzen und Übergabe prüfen

Wähle mit der Person einen echten kleinen Anlass, beispielsweise ein anstehendes Vorhaben oder eine konkrete Frage zu einer bestehenden Aufgabe. Trenne Gesprächsinput von bestätigter aktueller Wahrheit. Benenne den Owner, speichere nur nötige Fakten und leite einen nächsten Schritt ab. Erfinde weder Termine noch Zusagen.

Lies vor dem Anlegen das Profil und sein Template. Beim aktuellen Renderer müssen auch optionale Platzhalter im Template befüllt werden: Ist beispielsweise `project_phase` oder `commercial_state` nicht belegt, übergib einen leeren Renderwert und entferne die betreffende optionale Frontmatter-Zeile vor dem Speichern, wie es das Project-Template verlangt. Erfinde dafür keinen Geschäftsstatus. Eine Action braucht einen tatsächlichen Beleg in `evidence_refs`, etwa die passende Gesprächsquelle oder eine registrierte Working Note mit dem bestätigten Auftrag; eine leere Liste oder der Project-Owner allein ersetzt keinen Beleg. Prüfe den fertigen Record, nicht nur den erfolgreichen Renderbefehl.

1. Zeige die veränderten Dateien und erkläre in Alltagssprache, warum die Information dort liegt.
2. Prüfe betroffene Records mit dem Datenmodell-Werkzeug der installierten Instanz; der Ablauf steht in `docs/getting-started.md`. Behebe Fehler und prüfe erneut. Ein erfolgreicher Check ersetzt nicht die inhaltliche Rückmeldung.
3. Bitte um eine kurze inhaltliche Prüfung. Verarbeite eine tatsächliche Korrektur am Owner und den betroffenen Verweisen. Gibt es keinen Fehler, zeige, wie die Person eine spätere Änderung beauftragt; erfinde keinen Fehler für die Übung.
4. Gib einen kopierbaren Prompt für einen **neuen Chat im privaten Zielordner**: „Lies zuerst AGENTS.md und den dort verlinkten Startkontext. Finde den gespeicherten Kontext zu [unserem konkreten Anliegen], nenne die Quelldatei und den nächsten Schritt. Nutze keine Annahmen aus früheren Chats.“
5. Einen neuen Chat nur anlegen, wenn die Person das beauftragt. Sonst öffnet sie ihn selbst. Markiere die Übergabe erst als geprüft, wenn dieser Chat tatsächlich die richtigen Dateien gefunden hat; bis dahin bleibt sie offen.

Schließe mit Ergebnis, offenem Punkt, genau einem sinnvollen nächsten Schritt und dem Link zu `docs/first-week.md`. Ein neues Terminalfenster beweist keine Fortsetzung in einem unabhängigen Agentenchat.
