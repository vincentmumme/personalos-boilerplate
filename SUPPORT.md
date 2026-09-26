# Support

Die PersonalOS Boilerplate ist ein Open-Source-Projekt ohne garantierten individuellen Support oder Reaktionszeitraum.

## Wenn der Start hakt

Nutze zuerst [Lokal einrichten](docs/getting-started.md) und führe `doctor` mit demselben Python aus, mit dem du das CLI installiert hast. Die dortigen Beispiele gelten für macOS, Linux und Windows PowerShell. `doctor` liest, prüft und meldet konkrete nächste Schritte; er verbindet keine Accounts und verändert keine Dateien.

| Meldung oder Situation | Nächster Schritt |
| --- | --- |
| Agent kann den Repository-Link nicht lesen | ZIP herunterladen, vollständig entpacken und den lokalen Ordner im Agenten öffnen. Ohne Dateizugriff zunächst erklären und vorbereiten. |
| Python oder `pos_boilerplate` nicht gefunden | Python-Version prüfen und den direkten Interpreter aus `.venv` verwenden. CLI mit genau diesem Python installieren. |
| PowerShell blockiert die Aktivierung | Keine Aktivierung nötig: `.\.venv\Scripts\python.exe` direkt aufrufen. Keine Ausführungsrichtlinie ändern. |
| `ZoneInfoNotFoundError` oder fehlende Zeitzonendaten | Zonennamen prüfen; bei gültiger Zone `tzdata` mit demselben Python installieren und den Check wiederholen. |
| `manifest-hash-mismatch` | Vollständigen frischen Download prüfen. Unter Windows kann ein älterer Git-Checkout veränderte Zeilenenden enthalten; nutze einen frischen Checkout oder die ZIP-Datei. Den Manifest-Check nicht umgehen. |
| Ziel nicht leer | Eigenen neuen Zielordner wählen oder den Weg „Bestehendes verbessern“ nutzen. Keine vorhandenen Inhalte löschen. |
| Ziel innerhalb der Boilerplate | Privaten Zielordner außerhalb des öffentlichen Quellordners wählen. |
| Modul ist vorhanden, Dienst funktioniert noch nicht | In der [Modulübersicht](docs/modules.md) Voraussetzungen und Einrichtung prüfen. Installierte Anleitungen verbinden keinen Account. |
| Im neuen Chat fehlt Kontext | Prüfen, ob der private Zielordner geöffnet, `AGENTS.md` gelesen und der Kontext beim richtigen Owner gespeichert wurde. |

Eine Warnung zu fehlendem Git blockiert den Aufbau aus einer ZIP-Datei nicht. Ein erfolgreicher `doctor` bestätigt technische Voraussetzungen, keine Anmeldung, Kostenfreigabe oder funktionierende Sicherung. Wenn ein Problem bleibt, erstelle ein minimales Beispiel mit fiktiven Angaben.

## Einen Fehler nachvollziehbar melden

Nenne Betriebssystem, Python-Version, ZIP oder Clone, Boilerplate-Version beziehungsweise Release-Tag und den betroffenen Befehl mit neutralen Beispielpfaden. Beschreibe erwartetes und tatsächliches Ergebnis und füge die relevante bereinigte Fehlermeldung hinzu. Wenn möglich, reproduziere den Fehler mit der fiktiven Beispielinstallation in einem separaten Testordner.

Prüfe jeden Logauszug vor dem Teilen. Hänge weder dein persönliches PersonalOS noch die echten Installationswerte oder den privaten Onboarding-Zwischenstand an. Auch lokale Pfade und Terminalausgaben können Namen oder vertraulichen Inhalt enthalten.

## Der richtige Kanal

- Nutze [GitHub Issues](https://github.com/vincentmumme/personalos-boilerplate/issues) für reproduzierbare Fehler und konkrete technische Verbesserungsvorschläge.
- Nutze den [Mummentum Discord](https://discord.gg/T8MEvRtKB5) für Austausch, Erfahrungen und allgemeine Anwendungsfragen.
- Nutze GitHubs private Sicherheitsmeldung für Secrets, private Daten oder Schwachstellen. Der genaue Ablauf steht in [SECURITY.md](SECURITY.md).

## Bitte nicht veröffentlichen

Ein PersonalOS kann hochsensible Informationen enthalten. Teile in öffentlichen Kanälen niemals echte Kundeninhalte, Zugangsdaten, private IDs, persönliche Gesprächsausschnitte oder absolute private Pfade. Ersetze solche Werte in reproduzierbaren Beispielen durch eindeutig fiktive Daten.

Fragen zu individuell angepassten Installationen, externen Diensten oder privaten Automationen können in der Community besprochen werden, sind aber nicht Teil des garantierten Projektumfangs.
