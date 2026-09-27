# Lokal einrichten

Diese Anleitung führt vom Download zur geprüften Installation. Für die persönliche Auswahl und Fragen beginne bei [START-HERE.md](../START-HERE.md). Wer nur die Architektur verstehen möchte, braucht keine Installation.

Du brauchst Python ab 3.11 und eine Umgebung mit Dateizugriff und Terminal. Git ist beim ZIP-Download nicht nötig. Der Kern benötigt keine verbundenen Accounts, keinen Server und kein bestimmtes KI-Produkt. Ein Coding Agent kann diese Schritte im beauftragten Umfang für dich ausführen. Python-Pakete werden beim Setup aus dem konfigurierten Paketindex heruntergeladen.

## 1. Die Vorlage holen

Lade auf [GitHub](https://github.com/vincentmumme/personalos-boilerplate) über **Code → Download ZIP** die Vorlage herunter und entpacke sie vollständig. Öffne den Ordner, der `AGENTS.md`, `START-HERE.md`, `pyproject.toml`, `manifest.json` und `core/` enthält. Einzelne heruntergeladene Dateien reichen nicht.

Wenn du Git bereits nutzt, geht alternativ:

```text
git clone https://github.com/vincentmumme/personalos-boilerplate.git
```

Nutze eine Quelle, der du vertraust. Ein erfolgreicher Manifest-Check prüft die innere Konsistenz der Vorlage, nicht die Vertrauenswürdigkeit eines fremden Forks.

## 2. Das lokale Werkzeug vorbereiten

Alle weiteren Befehle laufen im entpackten oder geklonten Quellordner. Ersetze die beispielhaften Pfade durch deine tatsächlichen Pfade. Die virtuelle Python-Umgebung `.venv` hält die Werkzeuge dieses Projekts zusammen. Eine Aktivierung ist nicht nötig.

### macOS und Linux

```bash
cd "/Pfad/zur/personalos-boilerplate"
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m pos_boilerplate --help
```

Zeigt der zweite Befehl eine Version unter 3.11 oder fehlt Python, richte zuerst eine passende Version ein. Bei einer Linux-Meldung zu fehlendem `venv` nutze das zur Distribution gehörende Paket für diese Python-Version. Dein Agent kann die konkrete Meldung einordnen. Verwende keine systemweite Installation mit `sudo pip`.

### Windows PowerShell

```powershell
Set-Location "C:\Pfad\zur\personalos-boilerplate"
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pos_boilerplate --help
```

Falls `py` nicht vorhanden ist, verwende ein installiertes `python` ab 3.11 für die ersten beiden Python-Befehle. Fehlt Python ganz, installiere es zuerst. Die Schritte nutzen direkt `python.exe` in der virtuellen Umgebung; `Activate.ps1` und Änderungen an der PowerShell-Ausführungsrichtlinie sind nicht erforderlich.

Wenn ein Befehl fehlschlägt, behebe zuerst die angezeigte Ursache. Ein fehlgeschlagenes Paket-Setup lässt sich nicht durch den nächsten Installationsbefehl überspringen.

## 3. Privates Ziel und eigene Angaben wählen

Halte drei Orte auseinander:

| Ort | Zweck |
| --- | --- |
| `personalos-boilerplate/` | Öffentliche Vorlage und lokales CLI. Hier keine persönlichen Antworten eintragen. |
| Ein vereinbarter privater Setup-Ordner, etwa `PersonalOS-Setup/` neben der Vorlage | Eigene Installationswerte und optional der Zwischenstand. Er liegt außerhalb der Vorlage und des Installationsziels. |
| Ein privates Ziel, etwa `PersonalOS/` neben der Vorlage | Dein neues persönliches System. Der Ordner muss leer oder noch nicht vorhanden sein. Du darfst ihn vorher schon als Obsidian-Vault öffnen: `.obsidian/` und Systemdateien wie `.DS_Store` bleiben bei der Installation erhalten. |

Prüfe, dass diese Pfade nicht versehentlich in einem öffentlichen Repository oder einer unerwünscht geteilten Ablage liegen. Falls bereits Dateien im Ziel liegen, verwende den Weg „Bestehendes verbessern“ aus dem [Agentenablauf](../onboarding/agent-onboarding.md). Nichts zum Leeren des Ziels löschen.

Kopiere [onboarding/install-values.template.json](../onboarding/install-values.template.json) an den vereinbarten privaten Ort als `install-values.json`. Erstelle eine neue Datei; überschreibe keine bestehende Werte-Datei. Lass den Agenten die [passenden Fragen](../onboarding/intake.md) stellen oder bearbeite die Kopie selbst. Bestätige mindestens Anzeigename oder Pseudonym und den technischen `user_slug`. Unbekannte Texte dürfen „Noch nicht geklärt“ bleiben. Behalte gültiges JSON mit doppelten Anführungszeichen und ohne Kommentare bei.

`examples/install-values.example.json` enthält ein fiktives Profil. Nutze es nur für eine ausdrücklich fiktive Testinstallation. Übernimm daraus keine Eigenschaften für dein echtes PersonalOS.

## 4. Lesende Vorprüfung

Die folgenden Beispiele verwenden `../PersonalOS` als Ziel und `Europe/Berlin` als gewünschte Zeitzone. Passe beides an. Die Vorprüfung stellt keine Zeitzone um und verändert keine Dateien.

macOS / Linux:

```bash
.venv/bin/python -m pos_boilerplate doctor --build . --destination "../PersonalOS" --mode new --timezone Europe/Berlin
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pos_boilerplate doctor --build . --destination "..\PersonalOS" --mode new --timezone Europe/Berlin
```

Für einen bestehenden Ordner ersetze `--mode new` durch `--mode existing`. Das prüft die Grundlage für eine lesende Bestandsaufnahme und erlaubt keine Installation darüber. Bei einem reinen Verbesserungsauftrag ist kein neues CLI-Setup nötig, wenn die Bestandsaufnahme mit vorhandenen Werkzeugen ausreicht.

`doctor` prüft Python, Plattform, Zeitzonendaten, Git-Verfügbarkeit, Vorlage und Ziel. Exit-Code **0** bedeutet keine erkannten technischen Blocker; Hinweise können bleiben. Exit-Code **2** bedeutet mindestens einen Blocker. Mit `--json` erhält dein Agent dasselbe Ergebnis strukturiert. Der Check bestätigt weder angemeldete Accounts noch Modellzugriff, Preise, Agentenrechte oder eine funktionierende Sicherung. Tatsächliche Schreibfähigkeit wird erst beim Schreiben belegt.

Bei fehlenden Zeitzonendaten prüfe zuerst den Zonennamen. Wenn die Zone stimmt, installiere `tzdata` mit genau diesem Python:

```bash
.venv/bin/python -m pip install tzdata
```

Unter Windows lautet der entsprechende Aufruf `.\.venv\Scripts\python.exe -m pip install tzdata`. Führe danach `doctor` erneut aus. Spätere PersonalOS-Prüfungen müssen dieselbe vorbereitete Python-Umgebung verwenden oder ebenfalls Zugriff auf die benötigten Zeitzonendaten haben.

## 5. Aufbauen

Nach erfolgreicher Vorprüfung und geklärten Angaben installierst du den Kern. Die Beispiele erwarten deine private Werte-Datei in `PersonalOS-Setup/` neben dem Quellordner:

macOS / Linux:

```bash
.venv/bin/python -m pos_boilerplate install --build . --destination "../PersonalOS" --values "../PersonalOS-Setup/install-values.json"
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pos_boilerplate install --build . --destination "..\PersonalOS" --values "..\PersonalOS-Setup\install-values.json"
```

Für gewünschte Module ergänze beispielsweise `--module content --module codex`. Für den vollständigen öffentlichen Aufbau verwende stattdessen `--all-modules`. Ohne Modulargument bleibt es beim Kern. Die [Modulübersicht](modules.md) erklärt, was jeweils mitgeliefert wird und welche Einrichtung später nötig ist.

Der Installer prüft die Vorlage, baut das System zunächst separat auf und prüft sein Datenmodell. Erst bei Erfolg übergibt er es an das neue Ziel. Er überschreibt keinen bestehenden Bestand. Die Datei `.personalos-install.json` dokumentiert den installierten Stand, Module und Dateihashes; sie ist ein technischer Nachweis, keine Sicherung deiner Daten und kein automatischer Updater.

Wenn der Installer einen Fehler meldet, lies die konkrete Ursache. Bei einem nicht leeren Ziel zuerst dessen Inhalt und den gewählten Weg klären. Einen teilfertigen oder fremden Ordner nicht blind entfernen und die Prüfung nicht deaktivieren.

## 6. Öffnen, personalisieren und nutzen

Öffne **das private Ziel** im Agenten. Lass ihn `AGENTS.md` und die dort verlinkten Einstiegspunkte lesen. Kontrolliert gemeinsam `USER.md` und `identity/me.md`: Bekannte Angaben müssen stimmen, offene Punkte müssen offen erkennbar bleiben. Obsidian kannst du bei Bedarf auf denselben Ordner öffnen.

Danach bearbeitet ihr einen echten kleinen Anlass und speichert den nötigen Kontext nach den vorhandenen Templates. Für geänderte Records lässt sich die Prüfung aus dem Quellordner beispielsweise so ausführen:

```bash
.venv/bin/python "../PersonalOS/system/data-model/scripts/pos_v1.py" --root "../PersonalOS" validate --files USER.md identity/me.md
```

```powershell
.\.venv\Scripts\python.exe "..\PersonalOS\system\data-model\scripts\pos_v1.py" --root "..\PersonalOS" validate --files USER.md identity/me.md
```

Ersetze oder ergänze die Dateiliste durch die tatsächlich geänderten Records. Der Agent nutzt bei weiteren Arbeiten die Regeln und Prüfungen der installierten Instanz. Ein erfolgreicher technischer Check ersetzt nicht deine inhaltliche Prüfung.

Teste danach einen neuen Chat im privaten Ziel mit einem konkreten Anliegen:

```text
Lies zuerst AGENTS.md und den dort verlinkten Startkontext. Finde den gespeicherten Kontext zu [meinem konkreten Anliegen]. Nenne die Quelldatei und den nächsten Schritt. Nutze keine Annahmen aus früheren Chats.
```

Wenn das funktioniert, musst du deinen Kontext nicht erneut erzählen. Wenn etwas fehlt, korrigiert ihr die zuständige Datei und versucht es erneut. [Die erste Woche](first-week.md) hilft beim Benutzen, Sichern und späteren Erweitern. Bei technischen Problemen nutze [SUPPORT.md](../SUPPORT.md).
