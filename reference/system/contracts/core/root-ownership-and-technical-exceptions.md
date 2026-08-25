---
schema_version: pos-v1
id: 019ff134-cbdf-7232-be0b-3e4cc133135f
type: contract
title: "Root Ownership and Technical Exceptions"
created: 2026-08-11
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.2.0
---

# Root Ownership and Technical Exceptions

## Contract

Die Root-Ebene des PersonalOS ist eine geschlossene Governance-Fläche. Kanonische Roots besitzen eine eindeutige Wahrheitsklasse; registrierte technische Ausnahmen besitzen keine fachliche Wahrheit. Datei- oder Implementierungsformen legitimieren keinen Root.

## Scope

Der Vertrag gilt für alle sichtbaren und versteckten Verzeichnisse direkt unter dem PersonalOS-Ordner und für neue Root-Vorschläge.

## Invariants

- Der Pflichtkern besteht aus `inbox/`, `identity/`, `people/`, `companies/`, `projects/`, `interactions/`, `knowledge/`, `operations/`, `decisions/`, `daily/` und `system/`.
- `skills/` ist die ausführbare Capability-Schicht des Pflichtkerns. Sie besitzt keine persönliche oder fachliche Wahrheit.
- Optionale Domainmodule dürfen `business/`, `content/`, `finance/` und `health/` ergänzen. Ein nicht installiertes Modul ist kein fehlender Pflichtroot.
- Agenten, Hosts, Runtimes, Scheduler-Sollzustand, Systemzugriffe und Automationen bleiben Systemmetawahrheit unter `system/`. Ein Modul aktiviert keinen Dienst und legitimiert keinen gleichnamigen Root.
- `knowledge/` besitzt generalisierte, dauerhafte Knowledge Truth; domainspezifische operative Wahrheit bleibt bei der Domain.
- Scripts liegen beim funktionalen Owner: skilllokale Ausführung beim Skill, Domainruntime bei der Domain beziehungsweise Capability, Migrationscode beim Project oder Data Model und systemweite Checks beim Systemowner.
- Whiteboards liegen als Work Artifacts beim fachlichen Owner. `whiteboard/` ist kein Zielroot.
- Toolbedingt notwendige Punktordner wie `.git/`, `.obsidian/` und `.claude/` sind technische Root-Ausnahmen. Sie enthalten keine fachliche Wahrheit.
- `deals/`, `programs/`, `archive/`, `notes/`, `agents/`, `scripts/`, `assets/`, `docs/`, `outputs/`, `tmp/` und `whiteboard/` sind keine fachlichen Zielroots.
- Ein neuer Root benötigt eine nachgewiesene Modelllücke und die ausdrückliche Entscheidung des Nutzers.

## Interfaces

Der Root-Owner begrenzt erlaubte Profile und Pfade in der `pos-v1`-Registry. `INDEX.md` navigiert den aktuellen physischen Bestand. Physische Änderungen folgen dem PersonalOS Mutation Contract und einem vollständigen Link-, Consumer- und Recovery-Plan.

## Compliance

Ein Root ist nicht compliant, wenn sein Zweck nur Dateien einer Art, Outputs, Dokumente, Scripts oder temporäre Arbeit lautet. Cleanup darf keine reale Quelle, Evidenz, Decision, Planung oder Deliverable vernichten. Parallele aktive Wahrheiten sind verboten.

## Evolution

Technische Ausnahmen werden einzeln registriert. Ein kanonischer Root wird nur nach Root-Test, Alternativenprüfung, Decision Evidence, Registry-Propagation und ausdrücklicher Freigabe ergänzt oder entfernt.

## Change History

- **{{install_date}}** | Pflichtkern und optionale Domainroots für die Boilerplate getrennt; Contract auf 1.2.0 angehoben.
