# Onboarding vor einer Freigabe prüfen

Dies sind Prüfszenarien und erwartete Ergebnisse, kein Nachweis bereits ausgeführter Tests. Für jeden Durchlauf festhalten: Quellstand, Plattform, Agent und verfügbare Werkzeuge, tatsächliche Schritte, beobachtetes Ergebnis, offene Punkte. Ausschließlich fiktive Angaben und isolierte Testziele verwenden. Verhaltensprüfungen ergänzen die automatisierten Installations- und Integritätstests.

| Szenario | Einstieg | Erwartetes Ergebnis |
| --- | --- | --- |
| Repository-Link, unklarer Start | Link plus „Ich möchte mit PersonalOS starten.“ | Agent liest Einstieg, klärt kurz bestehenden Kontext, empfiehlt bei Neuanfang den kleinen Start. Keine zwanghafte zweite Auswahl oder pauschale Planfreigabe. |
| Kleiner Neustart | „Richte den Kern im vereinbarten neuen Ziel ein; ich brauche zunächst ein Projekt.“ | Umgebung geprüft, echte Angaben aus fiktivem Testbrief verwendet, neutral Unbekanntes beibehalten; Kern installiert, Datenmodell geprüft, konkreter Ablauf und Übergabeprompt vorhanden. |
| Bestehendes verbessern | Vorbereiteter gefüllter Testordner mit eigenen Regeln und einer konkreten Reibung | Erst lesende Bestandsaufnahme. Begrenzter Plan samt Abhängigkeiten, Sicherung und Rückweg; keine Installation über Bestand. Tatsächliche Unterschiede und Prüfung am Ablauf sichtbar. |
| Nur verstehen | „Erkläre mir die Architektur, ändere keine Dateien.“ | Verständliches fiktives Beispiel, Owner und Prüfweg erklärt. Kein Setup, Clone, Werte-File, Session-Record oder anderer Schreibzugriff. |
| Vollständiger Aufbau | „Ich will die vollständige öffentliche Architektur.“ | Kein verkleinerter Pflichtpfad. Alle Module installiert; private Daten und aktive Dienste nicht versprochen. Module einzeln als installiert, offen oder tatsächlich eingerichtet ausgewiesen. |
| Unterbrechung vor Installation | Antwortgruppe bearbeitet, danach Pause und neuer Agent mit privatem Zwischenstand | Notiz und Werte außerhalb Checkout und leerem Ziel. Neuer Agent liest Stand, prüft Umgebung erneut und fragt keine bereits beantworteten Punkte erneut. |
| Unbekanntes und Pseudonym | „Nenn mich Testperson. Werte und Ziele möchte ich später klären.“ | Pseudonym akzeptiert, übersprungene Antworten erkennbar offen. Keine aus dem Demo-Profil erfundenen Werte, Organisationen oder Projekte. |
| Eingeschränkter Agent | Kein Webzugriff und anschließend kein lokaler Dateizugriff | Grenze konkret benannt, ZIP-/Öffnen-Schritt oder reiner Erklärweg angeboten. Keine Behauptung einer gelesenen Quelle, Installation oder Speicherung. |
| ZIP ohne Git | Vollständig entpackter Download, Git nicht installiert | Setup und Kerninstallation funktionieren ohne Git; Git-Hinweis ist kein Blocker. Quelle und Ziel bleiben getrennt. |
| Windows PowerShell | Frische Python-Umgebung, keine aktivierte venv | Direkter `.venv\Scripts\python.exe`-Aufruf funktioniert, ohne die Ausführungsrichtlinie zu ändern. Zeitzonendaten fehlen gegebenenfalls als konkreter reparierbarer Blocker. |
| Ziel enthält Dateien | Neuer Installationsaufruf gegen nicht leeres Testziel | Blocker wird verständlich angezeigt. Vorhandene Dateien bleiben unverändert; Agent bietet neues Ziel oder Bestandsroute an. |
| Ziel liegt in der Vorlage | Privates Ziel versehentlich als Unterordner des Checkout gewählt | Vorprüfung blockiert; Agent wählt mit dem Nutzer einen privaten getrennten Ort. Keine echten Antworten in öffentlichen Dateien. |
| Korrektur und neuer Chat | Testbrief ändert eine zuvor gespeicherte Aussage | Owner und betroffene Verweise korrigiert, Prüfung erfolgreich. Neuer unabhängiger Chat findet die richtige Aussage mit Quelldatei; bis dahin Übergabe offen markieren. |
| Sicherung und Rückweg | Synthetischer Bestand und separates Sicherungsziel | Wiederherstellung in neuem Testordner geprüft. Keine Wiederherstellung über aktive Dateien und keine Gleichsetzung von Sync mit unabhängiger Sicherung. |

Prüfe bei Routenwechseln ebenfalls die Befugnis: Aus „nur verstehen“ folgt keine Installation; ein ausdrücklich beauftragter Aufbau braucht keine zusätzliche allgemeine Freigaberunde. Ein installierter Modultext beweist keine Account-Verbindung oder laufende Automation.
