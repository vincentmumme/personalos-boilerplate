---
schema_version: pos-v1
id: 01a01984-e1fb-7f0b-a256-cd16bd7f3c71
type: convention
title: "Claim-nahe Quellenplatzierung"
created: 2026-08-19
updated: 2026-08-19
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Claim-nahe Quellenplatzierung

## Convention

Eine Quelle oder Decision Evidence steht so nah wie möglich an der materiellen Aussage, die sie trägt. Der Leser und ein Agent müssen ohne Suche erkennen können, welche Evidenz welchen Claim belegt.

## Use When

Diese Convention gilt für Current Truth, Timeline-Einträge, Analysen, Knowledge-Artikel, Entity- und Domainrecords sowie belegorientierte Antworten aus dem PersonalOS. Sie gilt nicht für rein navigierende Indizes oder Aussagen, die ausschließlich die eigene Struktur des Records beschreiben.

## Default

- Ein einzelner Claim erhält den Quellenlink unmittelbar am Satzende.
- Ein vollständig durch dieselbe Evidenz getragener Absatz erhält den Quellenlink am Absatzende.
- Mehrere oder widersprüchliche Quellen werden direkt am betroffenen Claim gemeinsam genannt und in ihrer Aussagekraft unterschieden.
- Die profilgebundene `Sources`-Sektion bleibt als Quellenübersicht, Source Map oder ergänzende Provenance bestehen. Sie ersetzt keine claim-nahe Zuordnung.
- Eigene Ableitungen werden als Ableitung, Einschätzung oder Empfehlung markiert und nennen ihre Tatsachengrundlage.
- Fehlt eine belastbare Quelle, wird `unbelegt`, `unsicher` oder `nicht verifiziert` sichtbar gemacht.

## Allowed Variations

Tabellen dürfen eine eigene Quellen- oder Evidence-Spalte verwenden. Ein längerer Abschnitt darf nach einem einleitenden Scope-Satz eine gemeinsame Quellenangabe tragen, wenn eindeutig ist, dass sie den gesamten Abschnitt belegt. Rohquellen, Transkripte und unveränderliche Evidenz müssen sich nicht selbst zitieren, benötigen aber eindeutige Source Identity und Coverage.

## Examples

```markdown
{{organization_name}} wird von {{user_name}} und Alex Collaborator gemeinsam geführt. [[interactions/meetings/example/evidence/summary]]

Die Zusammenarbeit wurde am 12. August konkretisiert; der genaue operative Scope ist noch offen. [[decisions/2026/example-decision]]

Aus diesen beiden Signalen lässt sich eine steigende Priorität ableiten; das ist eine Einschätzung, keine bestätigte Entscheidung. [[interactions/conversations/example/evidence/message-batch]]
```

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
