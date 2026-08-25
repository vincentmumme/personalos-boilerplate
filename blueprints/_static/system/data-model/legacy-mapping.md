---
schema_version: pos-v1
id: "{{id_legacy_mapping}}"
type: data-model-document
title: "Legacy Mapping"
created: "{{install_date}}"
updated: "{{install_date}}"
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
document_kind: legacy-mapping
---

# Legacy Mapping

## Current Truth

Diese Installation startet ohne übernommene Legacy Records. Bestehende Daten aus anderen Systemen werden nicht mechanisch kopiert, sondern vor jeder Migration klassifiziert und einem kanonischen Owner sowie einem registrierten Zielprofil zugeordnet.

## Migration Rule

Kein Import ohne Inventar, Zielprofil, Feldtransformation, Pfad und Linkplan, Datenschutzprüfung, Recovery Möglichkeit und abschließende Verifikation.

## Local Mappings

Eigene Migrationsentscheidungen werden hier ergänzt, sobald tatsächlich ein bestehendes System übernommen wird.

## Timeline

• **{{install_date}}** | Neutrale Ausgangsbasis bei der Installation angelegt.
