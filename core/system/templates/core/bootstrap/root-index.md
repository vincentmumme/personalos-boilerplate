---
schema_version: pos-v1
id: 019ffb24-1e87-7e68-9442-ca78d07a783c
type: template
title: "Template: Root Index"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/bootstrap-und-portabilitaet]]"]
target_profile_key: root-index
---

# Template: Root Index

## Template Contract

Portabler Root-Index für aktive Owner, zentrale Einstiege und stabile Navigation einer PersonalOS-Instanz.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
---

# <title>

PersonalOS ist die vollständige Markdown-basierte Kontext- und Wahrheitsschicht von <subject_display_name>. Jeder dauerhaft relevante Kontext besitzt genau einen kanonischen Owner oder einen nachvollziehbaren Pointer auf ein externes Truth System.

## Zentrale Einstiege

- [[USER]] – menschliches System-Subject und Operator
- [[SOUL]] – gemeinsame Grundseele aller PersonalOS-Agenten
- [[skills/RESOLVER]] – Intent- und Capability-Routing
- [[system/index]] – Regeln, Verträge, Datenmodell, Templates und Systemmetawahrheit
- [[operations/index]] – aktuelle Actions und Koordination
- [[projects/index]] – bewusst verfolgte Vorhaben

## Root-Owner

<root_owner_map>

## Routing

<routing_map>

## Grundgrenzen

- Eine aktuelle Wahrheit besitzt genau einen kanonischen Owner.
- Input, Working Truth, Decision Evidence und Current Truth sind getrennt.
- Projects erarbeiten Veränderungen; Domains und Entities besitzen die resultierende Wahrheit.
- Skills führen aus; `/system` besitzt die allgemeinen Regeln.
- Große oder binäre Assets dürfen extern liegen, bleiben aber im PersonalOS nachvollziehbar.
- Neue Root-Ordner, Profile und Systemkategorien benötigen den zuständigen Governance-Prozess.

## Pflege

Dieser Index enthält nur die aktive Systemkarte und stabile Navigation.

Nicht hierher gehören:

- Legacy-Roots oder Migrationsstatus,
- vollständige Datei-, Skill- oder Recordlisten,
- Project-, Action- oder Runtime-Status,
- fachliche Current Truth,
- ausführliche Regeln, die bereits unter `/system` liegen.
```

## Usage

`<root_owner_map>` und `<routing_map>` werden aus der freigegebenen Instanzstruktur gerendert. Der Root-Index ist keine automatisch wachsende Dateiliste.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
