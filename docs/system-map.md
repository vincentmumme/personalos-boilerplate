# Karte des vollständigen Systems

Diese Seite ist die lesbare Navigation durch die PersonalOS Boilerplate. Sie fasst die Systemlogik nicht neu zusammen, sondern zeigt auf die Dateien, die sie tatsächlich besitzen.

## Die drei Produktschichten

| Schicht | Aufgabe | Einstieg |
| --- | --- | --- |
| Pflichtkern | allgemeine Struktur, Navigation, Systemverfassung, Datenmodell, Templates, Skills und Checks | [`core/`](../core/) |
| Optionale Module | zusätzliche Lebensbereiche, Werkzeuge, Agenten und Infrastruktur | [`modules/`](../modules/) |
| Vollständige Referenz | automatisch erzeugte Zusammensetzung aus Kern und allen Modulen | [`reference/`](../reference/) |

`reference/` ist keine dritte Wahrheit. Der Ordner zeigt das vollständige öffentliche System und wird aus den beiden anderen Schichten erzeugt.

## Die elf allgemeinen Bereiche

| Bereich | Besitzt |
| --- | --- |
| `inbox/` | neue Eingänge vor der Einordnung |
| `identity/` | bestätigten Kontext über die Person |
| `people/` | Menschen und Beziehungen |
| `companies/` | Organisationen und ihren aktuellen Kontext |
| `projects/` | Ziel, Scope, Arbeitsstand und Entscheidungen zeitlich begrenzter Vorhaben |
| `operations/` | Actions, Aufmerksamkeit und Ausführung |
| `decisions/` | bewusste Entscheidungen mit Begründung und Verlauf |
| `knowledge/` | Quellen und daraus aufbereitetes Wissen |
| `interactions/` | Gespräche, Nachrichten und andere Kontakte |
| `daily/` | Tageskontext und verdichtete Reflexion |
| `system/` | die Regeln, Modelle, Vorlagen und Prüfungen des PersonalOS selbst |

Die Root-Navigation einer Installation beginnt in [`core/INDEX.md`](../core/INDEX.md). Agenten starten über [`core/AGENTS.md`](../core/AGENTS.md), [`core/USER.md`](../core/USER.md) und [`core/SOUL.md`](../core/SOUL.md).

## Was in `system/` liegt

| Kategorie | Frage, die sie beantwortet | Einstieg |
| --- | --- | --- |
| Prinzipien | Welche Grundsätze ändern sich selten? | [`principles/`](../core/system/principles/) |
| Regeln | Welche klare Vorgabe gilt in einer konkreten Situation? | [`rules/`](../core/system/rules/) |
| Verträge | Welche Invarianten und Grenzen müssen immer gelten? | [`contracts/`](../core/system/contracts/) |
| Konventionen | Wie werden wiederkehrende Dinge einheitlich benannt und strukturiert? | [`conventions/`](../core/system/conventions/) |
| Frameworks | Wie wird eine komplexe Situation eingeordnet und entschieden? | [`frameworks/`](../core/system/frameworks/) |
| Templates | Welche Form braucht ein neuer Record? | [`templates/`](../core/system/templates/) |
| Runbooks | Welche Schritte führen einen bekannten Ablauf sicher aus? | [`runbooks/`](../core/system/runbooks/) |
| Checks | Wie wird Struktur oder Verhalten deterministisch geprüft? | [`checks/`](../core/system/checks/) |
| Datenmodell | Welche Record-Typen, Felder, Relationen und Schemas sind zulässig? | [`data-model/`](../core/system/data-model/) |
| Truth Systems | Welches System besitzt welche Wahrheit? | [`truth-systems/`](../core/system/truth-systems/) |
| Operating Systems | Welche übergeordneten Kontextsysteme sind registriert? | [`operating-systems/`](../core/system/operating-systems/) |

## Der zentrale Informationsfluss

Ein Agent behandelt neuen Input nicht sofort als aktuelle Wahrheit:

```text
Input oder externes Signal
  -> Quelle und Evidenz erhalten
  -> Bedeutung und Reifegrad bestimmen
  -> kanonischen Owner wählen
  -> betroffene Nachbarbereiche prüfen
  -> mit zuständiger Fähigkeit schreiben
  -> Struktur und Bedeutung verifizieren
```

Die tragenden Dateien dafür sind:

- [Source Provenance](../core/system/contracts/core/source-provenance.md) trennt Quelle, Analyse und aktuelle Wahrheit.
- [Context Routing and Truth Propagation](../core/system/frameworks/core/context-routing-and-truth-propagation.md) bestimmt Reifegrad, Owner und betroffene Nachbarbereiche.
- [Eine Wahrheit, ein kanonischer Owner](../core/system/principles/core/one-truth-one-owner.md) verhindert widersprüchliche aktive Wahrheitsorte.
- [PersonalOS Mutation Contract](../core/system/contracts/core/personalos-mutation-contract.md) bindet jeden Write an Scope, Provenance und Prüfung.
- [PersonalOS Mutation Runbook](../core/system/runbooks/core/personalos-mutation.md) führt den Ablauf praktisch aus.

## Datenmodell und Templates

Neue Records werden nicht frei erfunden. Ein registriertes Profil definiert den Typ, ein Template seine lesbare Form und die Datenmodell-Runtime erzeugt und prüft IDs, Felder und Relationen.

- [Profile](../core/system/data-model/profiles/)
- [Schemas](../core/system/data-model/)
- [kanonische Templates](../core/system/templates/)
- [Datenmodell-Runtime](../core/system/data-model/scripts/pos_v1.py)
- [Registry-Vertragstests](../core/system/data-model/tests/)

## Ausführung durch Skills

Skills sind ausführbare Fähigkeiten. Sie dürfen die Systemverfassung nicht neu definieren. Der Resolver führt einen Intent zur spezifischsten passenden Fähigkeit. Diese Fähigkeit arbeitet innerhalb der verlinkten Regeln und Verträge und endet mit der zuständigen Prüfung.

Der Pflichtkern bringt portable Einstiege für Verifikation, Aufgaben, Prioritäten, Logging, Skill-Entwicklung und lokale Call-Analyse mit. Agenten- und Runtime-spezifische Ergänzungen liegen als optionale Module vor.

## Optionale Bereiche

Der [Modulkatalog](../modules/catalog.json) enthält Domains wie Business, Content, Finanzen und Gesundheit sowie Adapter für Obsidian, Codex, Claude Code, Hermes, mehrere Agenten, externe Signale, Automationen, Git-Backups und mehrere Hosts.

Kein Modul ist standardmäßig aktiv. Ein Modul ergänzt den Kern, darf ihn aber nicht still überschreiben oder zu einer verdeckten Voraussetzung machen.

## Vollständigkeit und private Grenze

Vollständig bedeutet, dass jede versionierte Datei aus Vincents Referenzinstanz eine ausdrückliche Behandlung hat und wiederverwendbare Systemlogik nicht still verloren geht. Es bedeutet nicht, dass private Records, Secrets oder konkrete Laufzeitzustände veröffentlicht werden.

- [Produktvertrag](product-contract.md)
- [Abdeckungsübersicht](coverage.md)
- [Ableitungs- und Update-Modell](update-model.md)
- [Externe Systeme und Synchronisation](external-systems-and-sync.md)

## Gute Lesereihenfolge für einen Agenten

1. Für den Einstieg `AGENTS.md`, `START-HERE.md` und `onboarding/agent-onboarding.md` lesen.
2. Einen der vier Wege mit dem Nutzer wählen.
3. Diese Systemkarte verwenden, um nur die betroffenen Owner und Systemregeln zu lesen.
4. Bei einer Installation persönliche Angaben in kleinen Blöcken bestätigen lassen.
5. Vor jedem Write Scope, Owner und Prüfung benennen.
6. Nach dem Write die zuständigen Checks ausführen und das Ergebnis verständlich zeigen.
