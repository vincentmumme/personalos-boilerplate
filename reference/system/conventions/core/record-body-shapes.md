---
schema_version: pos-v1
id: 019ffc1a-c4f9-7baf-ae9a-fac53d810277
type: convention
title: "Record Body Shapes"
created: 2026-08-13
updated: 2026-08-22
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Record Body Shapes

## Convention

Die Body-Struktur einer Markdown-Datei wird ausschließlich durch ihr registriertes Primary Profile bestimmt. Current Truth plus Timeline ist Pflicht, wenn der Record einen über Zeit veränderlichen kanonischen Zustand besitzt; Quellen, Evidenz, Analyse, Decisions, Templates, Skills, Indizes, Views und andere Artefakte verwenden ihre eigene profilgebundene Shape.

## Use When

Bei jeder Erstellung oder materiellen Neufassung einer POS-verwalteten Markdown-Datei sowie bei der Entscheidung, ob Current Truth, Timeline, Change History, Sources oder andere Sektionen erforderlich sind.

## Default

- Kanonische Entities, Projects und fortlaufende Domainrecords verwenden eine kompakte Current Truth und eine datierte Timeline, wenn ihr Profil dies verlangt.
- Normative Artefakte verwenden die registrierten Kategorie-Sektionen und Change History.
- Evidence beschreibt Quelle und Coverage, nicht Current Truth.
- Analysen trennen Interpretation, Unsicherheit und Propagation.
- Indizes und Views bleiben Navigation beziehungsweise Ableitung.
- Narrative, Begründungen und Details gehören in den Body; kleine atomare Routing-/State-/Relationswerte in Frontmatter.

## Allowed Variations

Ein Profil darf Current Truth oder Timeline auslassen, anders benennen oder durch spezifischere Sektionen ersetzen. Die Variation wird im Page Shape/Profile registriert und nicht ad hoc in einer Instanz erfunden. Klassifizierte historische Legacy-Dateien dürfen ihre alte Shape als nicht-autoritative Evidenz behalten; aktive und neue Records folgen ausschließlich ihrem registrierten Zielprofil.

## Examples

- `person`, `company`, `project`: Current Truth plus Timeline nach registriertem Profile.
- `decision`: Outcome, Context, Rationale, Consequences und Evidence statt fortlaufender Truth-Timeline.
- `source-evidence`: Source Identity, Coverage, Extracted Evidence und Limitations.
- `skill`: Runtime-kompatible Skill-Struktur mit optionaler POS-Integration.
- `owner-index` oder `view-record`: Navigation, Source Owners, Derivation und Freshness.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
