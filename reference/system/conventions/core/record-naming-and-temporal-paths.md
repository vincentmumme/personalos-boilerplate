---
schema_version: pos-v1
id: 019ff208-1873-71be-bbfb-cc78f32e9037
type: convention
title: "Record Naming and Temporal Paths"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Record Naming and Temporal Paths

## Convention

PersonalOS trennt lesbare Navigation von stabiler Identität. Benannte dauerhafte Objekte verwenden kurze semantische Slugs; atomare, hochvolumige oder maschinell erzeugte Records verwenden die UUIDv7 aus ihrem Frontmatter als Dateinamen. Jeder konkrete Pfad wird durch das Primary Profile festgelegt und improvisiert keine eigene Benennungslogik.

## Use When

Diese Convention gilt beim Entwurf eines Profile-Pfadvertrags sowie beim Erstellen, Benennen, Partitionieren, Verschieben oder Umbenennen POS-verwalteter Dateien und Ordner. Sie gilt nicht für externe Assets, Provider-Dateinamen oder technische Toolartefakte, deren Format ein externer Vertrag besitzt.

## Default

### Slugs und strukturelle Namen

- Ordner und semantische Dateinamen verwenden ASCII-`lowercase-kebab-case`.
- Umlaute und `ß` werden als `ae`, `oe`, `ue` und `ss` transliteriert; Akzente werden entfernt.
- Strukturelle POS-Begriffe sind Englisch, beispielsweise `projects`, `working`, `decisions` und `evidence`. Inhaltliche Slugs folgen dem kanonischen Eigennamen oder der Sprache des Gegenstands.
- Collection- und Root-Ordner verwenden Plural, wenn sie mehrere gleichartige Records besitzen. Ein einzelner Record erhält keinen redundanten Typ-Suffix.
- `title` hält die vollständige menschenlesbare Bezeichnung. Der Pfad bleibt ein kurzer, stabiler Slug.
- Leerzeichen, Unterstriche, numerische Sortierpräfixe, wechselnde Großschreibung und Fortschrittsmarker wie `final`, `neu`, `v2` oder `copy` sind in kanonischen Slugs unzulässig.
- Etablierte technische Einstiegspunkte wie `INDEX.md`, `AGENTS.md`, `USER.md`, `SOUL.md`, `SKILL.md` und externe Toolkonventionen bleiben ausdrücklich registrierte Ausnahmen.

### Semantischer Slug oder UUID-Dateiname

- Benannte dauerhafte Entities, Projects, Domains und normative Artefakte verwenden semantische Slugs.
- Atomare Actions, Captures, Ideas, Contributions und vergleichbare kollisionsanfällige oder maschinell erzeugte Records verwenden ihre UUIDv7 als Dateinamen, sofern ihr Profile keinen begründeten chronologischen Pfad besitzt.
- Der Hauptrecord eines Project liegt als `projects/<project-slug>/<project-slug>.md` im stabilen Project-Namespace.
- Die UUID im Frontmatter bleibt immer die Record-Identität. Dateiname und Pfad werden niemals als Identitätsersatz verwendet.

### Datum und Zeit

- Reine Datumsfelder und Datumsbestandteile in Pfaden verwenden ausschließlich `YYYY-MM-DD`.
- Exakte Zeitpunkte verwenden RFC 3339 mit expliziter Zeitzone: `YYYY-MM-DDTHH:MM:SS+HH:MM` oder `Z`.
- `created` ist das unveränderliche logische Erstellungsdatum. `updated` ändert sich nur bei semantischer Record- oder contractrelevanter Metadatenänderung, nicht bei Zugriff, Formatierung, identischer Regeneration oder rein technischem Move.
- Ein Jahresordner wird nur verwendet, wenn das Profile eine dauerhaft wachsende chronologische Ereignis-, Beleg- oder Journalreihe besitzt. Das bloße Vorhandensein von `created` begründet keine Jahrespartition.
- Normale chronologische Reihen verwenden `<collection>/<year>/YYYY-MM-DD-<slug-or-id>`. Tagescontainer verwenden `daily/<year>/<date>/`.
- Zusätzliche Monatsordner sind kein spontaner Skalierungsmechanismus. Sie benötigen einen profilweiten, volumenbegründeten Pfadvertrag und gelten danach für die gesamte Record-Familie.

### Stabilität

- Eine Titeländerung benennt den Pfad nicht automatisch um.
- Ein Pfad wird nur geändert, wenn er fachlich falsch, dauerhaft irreführend oder Bestandteil einer kontrollierten Migration ist.
- Versionshistorie gehört in Git, Timeline, Revision oder ein registriertes Version-Profile und nicht in improvisierte kanonische Dateinamen.

## Allowed Variations

- Ein externer Standard darf Großschreibung, Dateiendung oder Namensform vorgeben, wenn das Artefakt als technische Ausnahme oder Companion Data klassifiziert ist und keine eigene POS-Norm behauptet.
- Ein Profile darf einen semantischen Slug mit Datum kombinieren, wenn Chronologie und menschliche Erkennbarkeit beide primäre Retrieval-Achsen sind, beispielsweise bei Decisions oder Meetings.
- Eine UUID kann zusätzlich zu einem Datumspräfix im Pfad stehen, wenn das Profile sowohl hohe Kollisionssicherheit als auch zeitliche Partitionierung benötigt.
- Abweichungen werden im Profile-Pfadvertrag begründet und gelten niemals nur für eine einzelne Instanz.

## Examples

```text
people/{{user_slug}}.md
companies/{{organization_slug}}.md
projects/beispielprojekt/beispielprojekt.md
operations/actions/019f0000-0000-7000-8000-000000000000.md
inbox/captures/019f0000-0000-7000-8000-000000000001.md
decisions/2026/2026-08-11-lesbare-pfade-stabile-ids-und-abgeleitete-sichten.md
daily/2026/2026-08-11/
interactions/meetings/2026/2026-08-11-{{organization_slug}}-weekly/
```

Nicht zulässige kanonische Pfade:

```text
projects/01_PersonalOS Final v2/
people/{{user_name}}.md
decisions/11.08.2026-neue-regel.md
system/rules/regel_neu_final.md
```

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
