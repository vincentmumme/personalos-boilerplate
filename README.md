# PersonalOS Boilerplate

[![CI](https://github.com/vincentmumme/personalos-boilerplate/actions/workflows/ci.yml/badge.svg)](https://github.com/vincentmumme/personalos-boilerplate/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/downloads/)
[![Lizenz: MIT](https://img.shields.io/badge/Lizenz-MIT-yellow.svg)](LICENSE)

Ein offenes, Markdown-basiertes Betriebssystem für deinen persönlichen Kontext. Es gibt dir und deinen KI-Agenten eine gemeinsame Grundlage für Projekte, Entscheidungen, Beziehungen, Regeln, Aufgaben und Wissen.

Die Boilerplate ist der öffentliche Einstieg in PersonalOS. Vincent hat sie direkt aus seinem real genutzten PersonalOS abgeleitet. Sie stellt dessen öffentlich portable Systembasis bereit: Struktur, Regeln, Datenmodelle, Templates, Prüfungen und Arbeitsweisen.

## In 30 Sekunden mit deinem Agenten starten

Gib deinem Agenten den Repository-Link und einen Satz:

```text
https://github.com/vincentmumme/personalos-boilerplate

Ich möchte mit PersonalOS starten.
```

Der Agent klärt dein Ziel, prüft deine Umgebung und führt dich mit wenigen passenden Fragen zum ersten eigenen Arbeitsablauf. Ein bereits klarer Auftrag wird direkt aufgegriffen. Du kannst klein anfangen, bestehende Dateien weiterentwickeln, das System erst verstehen oder vollständig aufbauen.

Alternativ: **Code → Download ZIP**, entpacken und den Ordner im Agenten öffnen. Git ist dafür nicht nötig. Der vollständige Ablauf steht in [START-HERE.md](START-HERE.md), die technischen Schritte für macOS, Linux und Windows in [Lokal einrichten](docs/getting-started.md).

## Was PersonalOS ist

PersonalOS ist eine lokale Kontext- und Wahrheitsschicht für Menschen und KI-Agenten. Im Kern ist es ein verständlicher Ordner aus Markdown-Dateien. Neben den eigentlichen Inhalten stehen dort die Regeln dafür, wo Informationen hingehören, welche Datei eine aktuelle Wahrheit besitzt und wie Änderungen geprüft werden.

Du kannst Obsidian als Oberfläche nutzen, musst es aber nicht. Codex, Claude Code und andere Coding Agents können direkt mit den Dateien arbeiten. Die Systemlogik bleibt unabhängig von einem einzelnen Anbieter, Agenten oder Gerät.

PersonalOS ist für Menschen gedacht, die ihren Kontext nicht in jeder Unterhaltung neu erklären möchten und trotzdem nachvollziehen wollen, was ihr Agent liest und verändert.

## Woher PersonalOS kommt

[Vincent Mumme](https://www.linkedin.com/in/vincentmumme/) hat PersonalOS aus seiner täglichen Arbeit mit KI-Agenten aufgebaut. Der Ausgangspunkt war ein praktisches Problem: Wichtiger Kontext lag in vielen Tools, Gesprächen und einzelnen Chats. Agenten konnten gute Aufgaben erledigen, aber ihnen fehlte eine dauerhafte gemeinsame Grundlage.

Aus dieser Arbeit entstand Schritt für Schritt ein System für persönlichen Kontext, Business, Content, Entscheidungen, Wissen und Ausführung. Vincent nutzt sein privates PersonalOS weiterhin als Referenzsystem. Diese Boilerplate überträgt die wiederverwendbare Architektur, Regeln, Templates und Arbeitsweisen in ein öffentliches Repository, ohne private Daten oder konkrete Zugangsdaten offenzulegen.

Die Hintergründe und Leitgedanken stehen in [Warum PersonalOS existiert](docs/philosophy.md).

## Welchen Ansatz das System verfolgt

- **Lesbare Dateien statt versteckter Memory-Schicht:** Du kannst jede Grundlage selbst öffnen, prüfen und ändern.
- **Eine Wahrheit, ein Owner:** Aktuelle Information liegt an genau einem kanonischen Ort. Andere Dateien verlinken dorthin.
- **Input ist noch keine Wahrheit:** Nachrichten, Calls und andere Signale bleiben zuerst nachvollziehbare Quellen. Erst bestätigte Aussagen werden in den zuständigen Kontext übertragen.
- **Projekte besitzen Arbeitskontext, Actions besitzen Ausführung:** So bleiben Planung, Entscheidungen und nächste Schritte auseinanderhaltbar.
- **Systemlogik und persönliche Daten bleiben getrennt:** Regeln und Templates können weiterentwickelt werden, ohne deinen eigenen Kontext zu überschreiben.
- **Jede Änderung endet mit einer Prüfung:** Ein Agent soll nicht nur schreiben, sondern auch nachweisen, dass Struktur, Links und Owner noch stimmen.
- **Werkzeuge sind Adapter:** Agenten, Editoren, externe Dienste und Hosts dürfen wechseln. Die PersonalOS-Dateien bleiben die gemeinsame Grundlage.

Die ausführliche [Systemkarte](docs/system-map.md) zeigt, wo diese Prinzipien als Regeln, Verträge, Frameworks, Templates, Runbooks und Checks umgesetzt sind.

## Vier mögliche Wege

1. **Klein neu starten:** Mit dem Kern, eigenem Kontext und nur den jetzt hilfreichen Modulen beginnen.
2. **Bestehendes verbessern:** Das eigene System erst verstehen und dann gezielt weiterentwickeln, mit Sicherung und nachvollziehbaren Änderungen.
3. **Erst verstehen:** Architektur und Entscheidungen erklären lassen, ohne Installation oder Dateiänderungen.
4. **Vollständig aufbauen:** Den Kern und alle öffentlichen Module mit eigenen Angaben einrichten; Dienste separat verbinden.

Du musst Vincents Struktur nicht blind kopieren. Die Boilerplate stellt die Systementscheidungen vollständig zur Verfügung. Du entscheidest gemeinsam mit deinem Agenten, was zu deiner Arbeit passt.

Zum Lesen genügt ein Browser oder Editor; die Installation braucht Python ab 3.11. Obsidian, Git, Server und zusätzliche Accounts sind optional. Die Boilerplate hat keine Lizenzkosten. KI-Anbieter und später verbundene Dienste können Kosten verursachen. Ein Cloud-Agent kann auch lokal gespeicherte Inhalte beim Verarbeiten an seinen Anbieter übertragen. [Module und Voraussetzungen](docs/modules.md) helfen bei der Auswahl.

## Was im Repository enthalten ist

| Bereich | Inhalt |
| --- | --- |
| `core/` | Installierbares Pflichtfundament mit Root-Bereichen, Regeln, Verträgen, Frameworks, Templates, Skills und Checks |
| `modules/` | Optionale Lebensbereiche, Werkzeuge, Agenten und Infrastruktur; kein Modul ist vorab aktiv |
| `reference/` | Vollständige, automatisch erzeugte Zusammensetzung aus Kern und allen Modulen |
| `onboarding/` | Geführte Auswahl, Fragen, Planung und Aufbau mit einem Coding Agent |
| `examples/` | Ausschließlich fiktive Installationswerte und Demo-Material |
| `policy/` und `blueprints/` | Nachvollziehbare Ableitung aus Vincents real genutztem PersonalOS |
| `src/` und `tests/` | Installer, Audit, Secret-Scan und automatisierte Prüfungen |

Der Pflichtkern legt elf allgemeine Bereiche an:

```text
inbox/        Eingang vor der Einordnung
identity/     Kontext über dich
people/       Menschen und Beziehungen
companies/    Organisationen
projects/     zeitlich begrenzte Vorhaben
operations/   Aufgaben und Aufmerksamkeit
decisions/    bewusste Entscheidungen
knowledge/    Quellen und aufbereitetes Wissen
interactions/ Gespräche und andere Kontakte
daily/        Tageskontext
system/       Regeln, Modelle, Vorlagen und Prüfungen
```

Die [Systemkarte](docs/system-map.md) erklärt den gesamten Aufbau. Die [Abdeckungsübersicht](docs/coverage.md) zeigt, welche Teile aus Vincents Referenzsystem übernommen, neutralisiert, modularisiert oder bewusst ausgeschlossen werden.

## Externe Systeme und mehrere Geräte

PersonalOS versucht nicht, jedes andere System zu ersetzen. E-Mail-Anbieter, Kalender, Buchhaltung, Secret Stores, Repositories, große Dateien und andere externe Quellen behalten ihre klare Zuständigkeit. PersonalOS speichert den nötigen Kontext, Belege oder Pointer und vermeidet eine zweite unkontrollierte Wahrheit.

Für mehrere Geräte gilt ein einfaches Betriebsmodell: Pro PersonalOS-Repository gibt es genau einen automatischen Git-Writer. Dieser Host synchronisiert den freigegebenen Textbestand mit GitHub. Andere Rechner dürfen den Arbeitsbestand lesen oder über einen getrennten Dateitransport erhalten, führen aber keinen zweiten automatischen Commit- oder Push-Prozess aus. Ob der kanonische Writer ein Mac Mini, ein VPS oder ein anderer dauerhafter Host ist, spielt für das Modell keine Rolle.

Der vollständige portable Vertrag mit Failover, Backups, externen Daten und Secret-Grenzen steht in [Externe Systeme und Synchronisation](docs/external-systems-and-sync.md).

## Vom Download zum eigenen System

Die [Schritt-für-Schritt-Anleitung](docs/getting-started.md) führt durch Download, Python-Setup, lesende Vorprüfung mit `doctor`, private Installationswerte und Aufbau. Sie enthält getrennte Befehle für macOS/Linux und Windows PowerShell, ohne Aktivierung der virtuellen Umgebung.

Dein persönlicher Zielordner liegt außerhalb der öffentlichen Vorlage und muss für eine Neuinstallation leer sein; einen schon als Obsidian-Vault geöffneten Ordner nimmt der Installer an und behält `.obsidian/`. Antworten und Installationswerte bleiben privat; die fiktiven Angaben aus `examples/` sind nur für Demos gedacht. Bei einem bestehenden System beginnt der Agent mit einer lesenden Bestandsaufnahme und einer begrenzten Verbesserung.

Danach prüft ihr einen eigenen Arbeitsablauf und öffnet einen neuen Chat, der den gespeicherten Kontext wiederfindet. [Deine erste Woche](docs/first-week.md) beschreibt einfache Routinen, Sicherung, Wiederherstellung und spätere Erweiterungen.

## Was vollständig bedeutet

Du bekommst die öffentlich portable Systembasis aus Vincents PersonalOS. Dazu gehören die enthaltene Struktur, Systemverfassung, Datenmodelle, Templates, Prüfungen und Arbeitsweisen. Jede versionierte Datei des verwendeten Referenzstands wird beim Ableiten erfasst und erhält eine ausdrückliche Behandlung. Die [Modulübersicht](docs/modules.md) trennt mitgelieferte Inhalte von Fähigkeiten, die erst eingerichtet werden müssen.

Die Boilerplate ist nicht dieselbe betriebsbereite Laufzeit wie Vincents persönliche Instanz. Seine Daten, Kundenkontexte, Accounts, Geräte, verbundenen Dienste, privaten Spezialfähigkeiten und laufenden Automationen sind nicht enthalten. Sie hängen von seiner konkreten Umgebung ab. Du verbindest stattdessen deine eigenen Daten, Dienste und Geräte mit derselben Systembasis.

Die genaue Abgrenzung steht im [Produktvertrag](docs/product-contract.md). Das [Ableitungs- und Update-Modell](docs/update-model.md) erklärt, wie neue Systemlogik kontrolliert aus der privaten Referenzinstanz in dieses Repository gelangt.

## Recording Demo

Das separate `personalos-demo` Repository ist Vincents sichere Oberfläche für Videos und Präsentationen. Es wird mit allen Modulen aus dieser Boilerplate gebaut. Vincents eigener öffentlicher Kontext bleibt real. Andere Menschen, Kunden, Unternehmen, Gespräche und Projekte sind ausdrücklich erfunden.

```bash
.venv/bin/python -m pos_boilerplate demo \
  --build . \
  --destination ../personalos-demo-build \
  --values examples/recording-demo/values.json \
  --fixtures examples/recording-demo/overlay
```

Auch dieser Befehl schreibt nur in ein leeres oder noch nicht vorhandenes Ziel. Er setzt die vorbereitete Python-Umgebung voraus; unter Windows verwende den in [Lokal einrichten](docs/getting-started.md) beschriebenen Interpreter und schreibe den Befehl in eine Zeile.

## Projektstatus und eigene Prüfung

Die Boilerplate ist ein junges Open-Source-Projekt. Die Architektur ist installierbar und wird gegen Struktur, Manifest, Links, Datenmodell, Datenschutzgrenzen und die vollständige Git-Historie geprüft. Der aktuelle Funktionsumfang und bekannte Grenzen stehen im [Changelog](CHANGELOG.md). Verhalten und Einstieg werden zusätzlich anhand der [Onboarding-Szenarien](onboarding/validation-scenarios.md) geprüft; die Szenarien selbst sind noch kein Ausführungsnachweis.

```bash
.venv/bin/python -m unittest discover -s tests -v

.venv/bin/python -m pos_boilerplate audit \
  --build . \
  --public-safe-terms policy/public-safe-terms.json

.venv/bin/python -m pos_boilerplate secret-scan \
  --repository . \
  --history
```

Diese Entwicklungsprüfungen setzen die vorbereitete Python-Umgebung voraus; die vollständige Git-Historie kann nur in einem Git-Checkout geprüft werden. Für eine ZIP-Installation genügt die technische Anleitung mit `doctor`. Installiere nur aus diesem Repository oder aus einem Fork, dessen Änderungen du geprüft hast. Der Installer verifiziert das Build-Manifest und führt anschließend den mitgelieferten Datenmodell-Check aus.

## Beitragen, Support und Sicherheit

- **Fehler und technische Verbesserungen:** [GitHub Issues](https://github.com/vincentmumme/personalos-boilerplate/issues)
- **Pull Requests:** Bitte zuerst [CONTRIBUTING.md](CONTRIBUTING.md) lesen.
- **Austausch und Anwendungsfragen:** [Mummentum Discord](https://discord.gg/T8MEvRtKB5)
- **Vertrauliche Sicherheitsprobleme:** [SECURITY.md](SECURITY.md)
- **Supportgrenzen:** [SUPPORT.md](SUPPORT.md)

Es gibt keinen garantierten individuellen Support oder Reaktionszeitraum. Veröffentliche niemals persönliche PersonalOS-Inhalte, Kundendaten oder Zugangsdaten in Issues, Pull Requests oder im Discord.

## Mehr über Vincent Mumme und Mummentum

Vincent Mumme entwickelt Systeme, mit denen Menschen und Unternehmen KI verlässlich in ihre echte Arbeit integrieren können. Sein Fokus liegt auf Kontext, klaren Zuständigkeiten, nachvollziehbaren Abläufen und Agenten, die darauf aufbauen können.

Mit [Mummentum](https://www.mummentum.de/) arbeitet Vincent an KI-Readiness, BusinessOS-Systemen und praktischen agentischen Arbeitsweisen. PersonalOS ist die persönliche Grundlage dieser Arbeit und zugleich das offene Referenzmodell, das in diesem Repository zugänglich wird.

- [Website](https://www.mummentum.de/)
- [YouTube](https://www.youtube.com/@mummentum)
- [LinkedIn](https://www.linkedin.com/in/vincentmumme/)
- [Instagram](https://www.instagram.com/vincentmumme/)
- [X](https://x.com/vincentmumme)
- [Newsletter](https://mummentum.beehiiv.com/subscribe)
- [Discord Community](https://discord.gg/T8MEvRtKB5)

## Lizenz

Code und öffentliche Inhalte stehen unter der [MIT-Lizenz](LICENSE). Copyright © Vincent Mumme.
