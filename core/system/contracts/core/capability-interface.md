---
schema_version: pos-v1
id: 019fec98-24ec-732a-9e1c-1bdcea74b746
type: contract
title: "Capability Interface"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.2.0
---

# Capability Interface

## Contract

Jede ausführbare Capability, die PersonalOS-Normen oder PersonalOS-Records konsumiert, trennt normative Abhängigkeiten, Record-I/O, Creation Blueprints, Capability-Aufrufe und Verification maschinenlesbar. Diese optionale POS-Schnittstelle wird innerhalb der kanonischen `SKILL.md` des Skills deklariert. Technische Runtime-Dateien, Provider-Payloads und lokale Implementierungsdetails sind nicht Teil des Record-I/O.

## Scope

Der Vertrag gilt zunächst für registrierte `skill`-Records mit tatsächlicher POS-Integration und perspektivisch für Agent Profiles und Automations. Er gilt für lesende, mutierende und orchestrierende POS-Capabilities. Eigenständige Skills ohne POS-Normen, POS-Record-I/O, POS-Templates oder POS-Checks bleiben vollständig gültige `SKILL.md`-Skills und müssen keine leere Capability-I/O-Schnittstelle vortäuschen.

## Invariants

- `system_refs` enthält ausschließlich direkte normative Dependencies.
- `reads_profile_keys` und `writes_profile_keys` enthalten nur registrierte Primary-Profile-Keys.
- `template_refs` enthält nur Templates, die von der Capability tatsächlich zur Record-Erzeugung verwendet werden.
- `invokes_skill_refs` enthält nur eigenständige Skills; Scripts, CLIs, Provider und Libraries bleiben Implementierungsdetails.
- `check_refs` enthält die Checks, die den Write oder das Capability-Ergebnis absichern.
- Ein Skill wird durch genau eine kanonische `skills/<skill>/SKILL.md` abgebildet; `CAPABILITY.md` oder ein zweiter zentraler Skillrecord sind nicht zulässig.
- Ein Skill, der PersonalOS-Records verändert, besitzt mindestens einen Eintrag in `writes_profile_keys` und `check_refs`.
- In `SKILL.md` werden diese semantischen Feldnamen innerhalb von `metadata` als `pos_system_refs`, `pos_reads_profile_keys`, `pos_writes_profile_keys`, `pos_template_refs`, `pos_invokes_skill_refs` und `pos_check_refs` serialisiert.
- Ein externer Seiteneffekt ist kein POS-Record-Write; die Skill-Schnittstelle verwendet deshalb kein generisches `mutating`-Feld.
- Ein Skill ohne die jeweilige POS-Schnittstelle lässt das entsprechende Feld vollständig weg; leere Platzhalter sind unzulässig.
- Eine Capability darf kein persistiertes Record-Shape lokal definieren, wenn es dafür ein Systemtemplate oder Profile gibt.

## Interfaces

| Feld | Frage | Kanonischer Target |
|---|---|---|
| `system_refs` | Welche Normen muss die Capability anwenden? | registrierte normative Systemrecords |
| `reads_profile_keys` | Welche POS-Record-Typen liest sie fachlich? | Registry Profile Keys |
| `writes_profile_keys` | Welche POS-Record-Typen erstellt oder verändert sie? | Registry Profile Keys |
| `template_refs` | Welche Creation Blueprints nutzt sie? | `template`-Records |
| `invokes_skill_refs` | Welche eigenständigen Capabilities orchestriert sie? | `skill`-Records |
| `check_refs` | Welche ausführbaren Assertions sichern sie ab? | `check`-Records |

Ein Feld wird nur aufgenommen, wenn die jeweilige POS-Schnittstelle existiert. Leere Platzhalter sind unzulässig. Das Registry-Modul `capability-io` besitzt Feldsemantik und Relationen; einzelne Skills besitzen nur ihre konkreten Werte. `name` ist der kanonische Runtime- und Capability-Key und wird nicht als `capability_key` dupliziert. Die Registry projiziert die geschlossene `pos_*`-Namespace auf diese semantischen Felder; andere Metadata-Namespaces begründen keine POS-Schnittstelle.

## Compliance

Die Registry validiert Profile Keys, Relation Targets und die Conditional Rule für POS-mutierende Skills. Vor der Migration eines POS-integrierten Legacy-Skills müssen dessen Outputs, Templates und Checks inventarisiert sein. Fehlt ein Profile, Template oder Check, wird zuerst dessen Admission-Paket materialisiert; der Skill darf keine lokale Ersatznorm etablieren. Eigenständige Skills ohne POS-Schnittstelle werden dadurch nicht künstlich zu POS-Consumern.

## Evolution

Neue Capability-Facetten werden nur als Registry-Feld aufgenommen, wenn sie Routing, Ownership, Zugriff, Verification oder stabile maschinenlesbare Verknüpfung ermöglichen und nicht aus bestehenden Feldern ableitbar sind. Provider-, Tool- und Runtime-Abhängigkeiten rechtfertigen ohne POS-semantische Wirkung kein universelles Feld.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
