# Starte hier

Dieses Repository ist der öffentliche Einstieg in PersonalOS. Es enthält die vollständige öffentlich portable Systemlogik aus Vincent Mummes Referenzsystem: Ordner, Regeln, Verträge, Frameworks, Templates, Runbooks, Checks und optionale Erweiterungen. Private Daten, konkrete Accounts, Secret-Werte und aktive Laufzeiten gehören bewusst nicht dazu.

## Am einfachsten mit einem Coding Agent

Gib Codex, Claude Code oder einem anderen Coding Agent den Repository-Link und schreibe:

```text
Lies zuerst AGENTS.md und START-HERE.md in diesem Repository. Zeige mir danach die vier möglichen Wege, hilf mir bei der Auswahl und ändere noch keine Dateien.
```

Der Agent liest die eingebauten Arbeitsregeln, erklärt dir die vier Wege und zeigt einen kurzen Plan. Erst nach deiner Auswahl und Bestätigung baut er etwas auf.

## Die vier Wege

1. **Vollständiges PersonalOS:** Kern und alle Module als Ausgangspunkt nutzen.
2. **Kern mit Auswahl:** Pflichtfundament aufbauen und nur passende Module ergänzen.
3. **Verstehen:** Architektur, Regeln und Abwägungen erklären lassen, ohne Installation.
4. **Teile übernehmen:** Einzelne Frameworks, Regeln oder Templates in dein System übertragen.

## Lokal ausprobieren

Du brauchst Git und Python 3.11 oder neuer.

```bash
git clone https://github.com/vincentmumme/personalos-boilerplate.git
cd personalos-boilerplate
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

Danach kannst du deinem Coding Agent den lokalen Ordner geben oder mit den fiktiven Beispielwerten eine vollständige Testinstallation erzeugen:

```bash
pos-boilerplate install \
  --build . \
  --destination ../PersonalOS-example \
  --values examples/install-values.example.json \
  --all-modules
```

Der Zielordner muss leer oder noch nicht vorhanden sein. Für dein echtes PersonalOS ersetzt der Agent die Beispielwerte ausschließlich durch Angaben, die du selbst bestätigt hast.

## Was wo liegt

- `core/` enthält das Pflichtfundament und funktioniert ohne externe Dienste.
- `modules/` enthält optionale Bereiche wie Content, Gesundheit, Codex, Hermes, externe Signale oder mehrere Hosts.
- `reference/` zeigt die vollständige Zusammensetzung aus Kern und allen Modulen.
- `examples/` enthält fiktive Werte und später vollständige Demo-Abläufe.
- `onboarding/` beschreibt die Zusammenarbeit mit deinem Agenten.

Du musst Vincents Struktur nicht blind kopieren. Sie gibt dir alle Entscheidungen und Systemlogiken als Ausgangspunkt. Du entscheidest, was zu deiner Arbeit passt.

## Wenn du tiefer einsteigen willst

- [Warum PersonalOS existiert](docs/philosophy.md)
- [Karte des vollständigen Systems](docs/system-map.md)
- [Externe Systeme und Synchronisation](docs/external-systems-and-sync.md)
- [Produktvertrag und klare Grenzen](docs/product-contract.md)
- [Abdeckung der privaten Referenzinstanz](docs/coverage.md)

Bei Installationsfehlern nutze [GitHub Issues](https://github.com/vincentmumme/personalos-boilerplate/issues). Für Austausch und Anwendungsfragen gibt es den [Mummentum Discord](https://discord.gg/T8MEvRtKB5). Es besteht kein individueller Supportanspruch.
