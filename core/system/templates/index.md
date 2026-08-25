---
schema_version: pos-v1
id: 01a00117-59f7-7f89-a4b6-6300ead1607f
type: owner-index
title: "System Templates"
created: 2026-04-14
updated: 2026-08-14
index_scope: section
---

# System Templates

## Purpose

Dieser Ordner hält normative Instanz-Blueprints registrierter Primary Profiles. Jedes Template ist selbst ein `pos-v1`-Record mit `type: template`, verweist auf genau ein `target_profile_key` und lädt seine allgemeine Systemsemantik über `system_refs`.

## Ownership and Boundaries

Feld-, Enum-, Pfad- und Validierungsregeln werden niemals im Template oder Index dupliziert. Persistierte POS-Record-Templates werden auch dann hier geführt, wenn aktuell nur ein Skill sie konsumiert. Skilllokale Scripts, Provider-Payloads, Prompts, Testdaten oder externe Tool-Assets sind keine POS-Record-Templates. Sobald ein Artefakt Frontmatter, Pfad oder Body Shape einer persistierten POS-Datei vorgibt, wird es über ein registriertes Profile hierher migriert.

## Navigation

### Core und Project

- [[system/templates/core/bootstrap/agent-entry]]
- [[system/templates/core/bootstrap/claude-adapter]]
- [[system/templates/core/bootstrap/root-index]]
- [[system/templates/core/bootstrap/user-context]]
- [[system/templates/core/bootstrap/agent-persona]]
- [[system/templates/core/owner-index]]
- [[system/templates/project]]
- [[system/templates/working-note]]
- [[system/templates/redirect]]
- [[system/templates/truth-system]]

### Operations und Capture

- [[system/templates/action]]
- [[system/templates/attention-trigger]]
- [[system/templates/action-candidate]]
- [[system/templates/capture]]
- [[system/templates/idea]]

### Daily

- [[system/templates/daily/day-record]]
- [[system/templates/daily/activity-contribution]]
- [[system/templates/daily/journal-entry]]
- [[system/templates/daily/daily-briefing]]
- [[system/templates/daily/context-gap-review]]

### Identity und Entities

- [[system/templates/identity/identity-record]]
- [[system/templates/identity/biography]]
- [[system/templates/identity/personal-constitution]]
- [[system/templates/identity/operating-profile]]
- [[system/templates/identity/life-orientation]]
- [[system/templates/identity/legal-identity]]
- [[system/templates/identity/capabilities]]
- [[system/templates/entities/person]]
- [[system/templates/entities/company]]

### Business

- [[system/templates/business/brand]]
- [[system/templates/business/market]]
- [[system/templates/business/customer-profile]]
- [[system/templates/business/product]]
- [[system/templates/business/offer]]
- [[system/templates/business/business-model]]
- [[system/templates/business/strategy]]
- [[system/templates/business/operating-model]]
- [[system/templates/business/brand-voice]]
- [[system/templates/business/brand-design-system]]

### Interactions und Automations

- [[system/templates/interactions/interaction-event]]
- [[system/templates/interactions/conversation-stream]]
- [[system/templates/interactions/source-evidence]]
- [[system/templates/interactions/interaction-analysis]]
- [[system/templates/interactions/signal-digest]]
- [[system/templates/interactions/processing-receipt]]
- [[system/templates/automations/automation]]
- [[system/templates/automations/automation-run-receipt]]
- [[system/templates/automations/automation-day-summary]]

### Knowledge

- [[system/templates/knowledge/knowledge-topic]]
- [[system/templates/knowledge/knowledge-source]]
- [[system/templates/knowledge/knowledge-article]]
- [[system/templates/knowledge/knowledge-inventory-item]]
- [[system/templates/knowledge/knowledge-dataset]]
- [[system/templates/knowledge/knowledge-assessment]]
- [[system/templates/knowledge/knowledge-log]]

### Health

- [[system/templates/health/health-provider-snapshot]]
- [[system/templates/health/health-daily-assessment]]
- [[system/templates/health/health-operating-model]]
- [[system/templates/health/health-profile]]
- [[system/templates/health/health-plan]]
- [[system/templates/health/health-measurement]]

### Finance

- [[system/templates/finance/finance-account]]
- [[system/templates/finance/finance-payment-source-registry]]
- [[system/templates/finance/finance-expense]]
- [[system/templates/finance/finance-client-cost]]
- [[system/templates/finance/finance-time-entry]]
- [[system/templates/finance/finance-invoice]]
- [[system/templates/finance/finance-recurring-obligation]]
- [[system/templates/finance/finance-tax-dossier]]
- [[system/templates/finance/finance-tax-manifest]]

### Systemtopologie

- [[system/templates/topology/agent]]
- [[system/templates/topology/agent-persona-overlay]]
- [[system/templates/topology/runtime]]
- [[system/templates/topology/host]]
- [[system/templates/topology/system-service]]
- [[system/templates/topology/integration]]
- [[system/templates/topology/access-record]]
- [[system/templates/topology/operating-system]]
- [[system/templates/topology/view-record]]
- [[system/templates/topology/system-observability-view]]

### Normative Systemkategorien

- [[system/templates/principle]]
- [[system/templates/rule]]
- [[system/templates/contract]]
- [[system/templates/convention]]
- [[system/templates/framework]]
- [[system/templates/template]]
- [[system/templates/runbook]]
- [[system/templates/check]]
- [[system/templates/skill]]
- [[system/templates/skills/cron-prompt]]
- [[system/templates/skills/skill-reference]]
- [[system/templates/skills/skill-resolver]]

### Data Model

- [[system/templates/data-model/data-model-document]]
- [[system/templates/data-model/data-model-changelog]]
- [[system/templates/data-model/legacy-schema-pack]]

## Maintenance

Der erste eingezäunte Markdown-Block eines Template-Records ist die von der Registry-Runtime gerenderte Instanzvorlage. Überschriften innerhalb des Blueprints zählen nicht zum Body Shape des äußeren Template-Records. Neue Templates werden erst nach Registry-Admission ihres Zielprofils verlinkt; flache historische Pilotpfade werden nur in kontrollierten Consumer-Cutovers verschoben.
