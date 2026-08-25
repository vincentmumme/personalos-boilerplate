---
schema_version: pos-v1
id: 019ff59c-309e-78db-8f45-3340f29acd99
type: template
title: "Template: Interaction Event"
created: 2026-08-12
updated: 2026-08-12
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/frameworks/interactions/signal-evidence-und-processing]]"]
target_profile_key: interaction-event
---

# Template: Interaction Event

## Template Contract

Hauptrecord eines einmaligen Gesprächs, Calls, Workshops oder Treffens. Er beschreibt das Ereignis und seine belegten Ergebnisse, besitzt aber keine zweite fachliche Current Truth.

## Blueprint

```markdown
---
schema_version: <schema_version>
id: <id>
type: <type>
title: "<title>"
created: <date>
updated: <date>
interaction_date: <interaction_date>
interaction_kind: <interaction_kind>
participant_refs: <participant_refs>
evidence_refs: <evidence_refs>
---

# <title>

## Event

<what happened and the evidence boundary>

## Outcome

<source-bounded outcome>

## Commitments

<confirmed commitments or none>

## Open Questions

<unresolved points or none>

## Propagation

<updated, referenced and no-op owners>

## Sources

<source evidence links>

## Corrections

None.
```

## Usage

Der Hauptrecord liegt unter `interactions/meetings/<year>/YYYY-MM-DD-<slug>/YYYY-MM-DD-<slug>.md`. Evidence und Analysis sind getrennte Companion Records.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
