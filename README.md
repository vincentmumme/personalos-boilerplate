# PersonalOS Boilerplate

[![CI](https://github.com/vincentmumme/personalos-boilerplate/actions/workflows/ci.yml/badge.svg)](https://github.com/vincentmumme/personalos-boilerplate/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/downloads/)
[![Lizenz: MIT](https://img.shields.io/badge/Lizenz-MIT-yellow.svg)](LICENSE)

Ein offenes, Markdown-basiertes Betriebssystem für deinen persönlichen Kontext. Es gibt dir und deinen KI-Agenten eine gemeinsame Grundlage für Projekte, Entscheidungen, Beziehungen, Regeln, Aufgaben und Wissen.

Die Boilerplate ist der öffentliche Einstieg in PersonalOS. Vincent hat sie direkt aus seinem real genutzten PersonalOS abgeleitet. Sie stellt dieselbe Systembasis bereit: Struktur, Regeln, Datenmodelle, Templates, Prüfungen und Arbeitsweisen.

## In 30 Sekunden mit deinem Agenten starten

Gib deinem Coding Agent diesen Repository-Link:

```text
https://github.com/vincentmumme/personalos-boilerplate
```

Sende direkt danach diesen Prompt:

```text
Lies zuerst AGENTS.md und START-HERE.md in diesem Repository. Zeige mir danach die vier möglichen Wege, hilf mir bei der Auswahl und ändere noch keine Dateien.
```

Der Agent liest die eingebauten Arbeitsregeln, erklärt dir die möglichen Einstiege und zeigt einen kurzen Plan. Erst wenn du einen Weg gewählt und den Plan bestätigt hast, schreibt er Dateien. Der vollständige Ablauf steht in [START-HERE.md](START-HERE.md).

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

1. **Vollständig aufbauen:** Kern und alle Module als Ausgangspunkt verwenden.
2. **Gezielt aufbauen:** Mit dem Pflichtkern beginnen und nur passende Module ergänzen.
3. **Erst verstehen:** Architektur und Entscheidungen erklären lassen, ohne Dateien anzulegen.
4. **Einzelne Teile übernehmen:** Regeln, Frameworks oder Templates in ein bestehendes System übertragen.

Du musst Vincents Struktur nicht blind kopieren. Die Boilerplate stellt die Systementscheidungen vollständig zur Verfügung. Du entscheidest gemeinsam mit deinem Agenten, was zu deiner Arbeit passt.

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

## In fünf Minuten lokal ausprobieren

Du brauchst Git und Python 3.11 oder neuer.

```bash
git clone https://github.com/vincentmumme/personalos-boilerplate.git
cd personalos-boilerplate
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .

pos-boilerplate install \
  --build . \
  --destination ../PersonalOS-example \
  --values examples/install-values.example.json \
  --all-modules
```

Der Zielordner muss leer oder noch nicht vorhanden sein. Die Beispielinstallation enthält ausschließlich fiktive Werte. Für dein echtes PersonalOS übernimmt der Agent nur Angaben, die du selbst bestätigt hast.

## Was vollständig bedeutet

Du bekommst mit der Boilerplate 1:1 dieselbe Systembasis, mit der Vincent arbeitet. Für die enthaltenen Bereiche gelten dieselbe Struktur, dieselben Templates und dieselbe Logik. Dazu gehören Systemverfassung, Datenmodelle, Prüfungen, Arbeitsweisen und die mitgelieferten Fähigkeiten. Jede versionierte Datei aus Vincents PersonalOS wird beim Ableiten erfasst und erhält eine ausdrückliche Behandlung.

Die Boilerplate ist nicht dieselbe betriebsbereite Laufzeit wie Vincents persönliche Instanz. Seine Daten, Kundenkontexte, Accounts, Geräte, verbundenen Dienste, privaten Spezialfähigkeiten und laufenden Automationen sind nicht enthalten. Sie hängen von seiner konkreten Umgebung ab. Du verbindest stattdessen deine eigenen Daten, Dienste und Geräte mit derselben Systembasis.

Die genaue Abgrenzung steht im [Produktvertrag](docs/product-contract.md). Das [Ableitungs- und Update-Modell](docs/update-model.md) erklärt, wie neue Systemlogik kontrolliert aus der privaten Referenzinstanz in dieses Repository gelangt.

## Recording Demo

Das separate `personalos-demo` Repository ist Vincents sichere Oberfläche für Videos und Präsentationen. Es wird mit allen Modulen aus dieser Boilerplate gebaut. Vincents eigener öffentlicher Kontext bleibt real. Andere Menschen, Kunden, Unternehmen, Gespräche und Projekte sind ausdrücklich erfunden.

```bash
pos-boilerplate demo \
  --build . \
  --destination ../personalos-demo-build \
  --values examples/recording-demo/values.json \
  --fixtures examples/recording-demo/overlay
```

Auch dieser Befehl schreibt nur in ein leeres oder noch nicht vorhandenes Ziel.

## Projektstatus und eigene Prüfung

Version `0.1.0` ist der erste vorgesehene öffentliche Stand. Die Architektur ist installierbar und wird gegen Struktur, Manifest, Links, Datenmodell, Datenschutzgrenzen und die vollständige Git-Historie geprüft. Der aktuelle Funktionsumfang und bekannte Grenzen stehen im [Changelog](CHANGELOG.md).

```bash
python3 -m unittest discover -s tests -v

pos-boilerplate audit \
  --build . \
  --public-safe-terms policy/public-safe-terms.json

pos-boilerplate secret-scan \
  --repository . \
  --history
```

Installiere nur aus diesem Repository oder aus einem Fork, dessen Änderungen du geprüft hast. Der Installer verifiziert das Build-Manifest und führt anschließend den mitgelieferten Datenmodell-Check aus.

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
