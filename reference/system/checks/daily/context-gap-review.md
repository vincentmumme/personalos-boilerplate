---
schema_version: pos-v1
id: 01a00165-1104-703e-bd96-4095d8731e86
type: check
title: "Context Gap Review Check"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/daily/context-gap-review-ownership-and-propagation]]", "[[system/templates/daily/context-gap-review]]"]
check_kind: content
verifies_refs: ["[[system/contracts/daily/context-gap-review-ownership-and-propagation]]", "[[system/contracts/normative-system-architecture]]"]
---

# Context Gap Review Check

## Purpose

Der Check sichert Profil, Tageszuordnung, Parent Day, Zeitzone, Platzhalterfreiheit sowie die vollständige Form eines Question Batch.

## Assertions

- Der Record besteht gegen `pos-v1` inklusive Relations- und Parent-Day-Auflösung.
- Ein `question-batch` enthält genau die nummerierten Fragen 1 bis 5.
- Jede Frage enthält Frage, Warum jetzt, Evidenz, Verbesserung, Write-back-Ziel, Antwortformat, Sensitivität und Score.
- Andere Review-Arten verwenden dasselbe Recordprofil, benötigen aber keine künstliche Fünferzahl.
- Unaufgelöste Template-Platzhalter sind blockierend.

## Implementation

Die portable Basisprüfung nutzt das öffentliche Datenmodell für Profil, Pfad, Pflichtfelder und Relationsauflösung. Eine Installation kann ergänzend einen fokussierten Context-Gap-Reviewer als eigene Capability hinzufügen.

## Invocation

```bash
python3 system/data-model/scripts/pos_v1.py --root . validate --files <daily-context-gap-review> --json
```

## Outcomes

Jeder Fehler blockiert Abschluss und Propagation des Review-Runs. Ein erfolgreicher Check autorisiert keine fachliche Current Truth; diese bleibt an den Mutation Contract und den kanonischen Owner gebunden.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
