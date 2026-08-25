---
schema_version: pos-v1
id: 019ffb24-1eb9-7919-a2b9-1fb2b8778068
type: template
title: "Template: User Context"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/bootstrap-und-portabilitaet]]"]
target_profile_key: user-context
---

# Template: User Context

## Template Contract

Portabler kompakter Startkontext über das menschliche System-Subject. Die vollständige Wahrheit bleibt beim Record in `<subject_ref>`.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
subject_ref: "<subject_ref>"
---

# <title>

Diese Datei ist der kompakte Startkontext über <subject_display_name> als Mensch und Operator. Die vollständige kanonische Identitätswahrheit liegt unter <subject_ref>.

## Kurzprofil

<short_profile>

## Arbeitsweise und Denkstil

<work_style>

## Entscheidungen

<decision_style>

## Arbeitsbeziehung mit Agenten

<agent_relationship>

## Wichtige Beziehungen und Rollen

<relationships_and_roles>

## Werte und Haltung

<values_and_attitude>

## Wahrheitskarte

<truth_map>

## Pflege

Diese Datei enthält nur stabilen, agentenrelevanten Startkontext.

Nicht hierher gehören:

- ausführliche Identity-, Legal-, Business- oder Domainwahrheit,
- aktuelle Projects und Actions,
- Timeline und Tagesereignisse,
- Agenten- oder Systemregeln,
- sensible Identifikatoren oder Secrets,
- häufig wechselnde Statusinformationen.

Wenn sich eine dauerhaft agentenrelevante Wahrheit über <subject_display_name> materiell ändert, wird zuerst der kanonische Owner und anschließend diese Projektion aktualisiert.
```

## Usage

Alle Inhaltsplätze werden aus der konkreten Instanz kuratiert. Das Template enthält keine Beispielbiografie und keine persönlichen Werte eines Boilerplate-Autors.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
