---
schema_version: pos-v1
id: 019ff118-a2ab-7569-b764-30ee1186cd54
type: framework
title: "Capture-Retention und Promotion"
created: 2026-08-11
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Capture-Retention und Promotion

## Purpose

Dieses Framework bewahrt relevanten Input verlustfrei, verhindert aber die dauerhafte Speicherung jeder beiläufigen Äußerung und jedes technischen Zwischenprodukts.

## Model

```text
Input
  -> Source-, Nuancen-, Audit- und Sensitivitätsrisiko bestimmen
  -> bis zur erfolgreichen Verarbeitung bewahren
  -> Delta und Owner propagieren
  -> Retention entscheiden:
       raw behalten | redigieren | stabil verweisen | verlustfrei verdichten | verwerfen
  -> bei dauerhafter Bedeutung gezielt promoten
```

Capture, Source Evidence, Processing Receipt, Idea, Action, Project und Current Truth bleiben verschiedene Reifegrade beziehungsweise Objektklassen.

## Components

- **Unprocessed Capture:** darf nicht gelöscht werden.
- **Raw oder redigierte Evidence:** bleibt bei materiellem Beweis-, Nuancen- oder Auditwert erhalten.
- **Processing Receipt:** nur bei Multi-Owner-Propagation, Automation, Partial Failure oder Auditbedarf.
- **Compacted Capture:** darf Raw ersetzen, wenn Source-Basis und relevante Nuance vollständig erhalten bleiben.
- **Promotion:** bewusster Übergang zu Idea, Action, Project, Knowledge oder fachlicher Current Truth.
- **Discard:** erst nach erfolgreicher Verarbeitung und nachweisbar fehlendem Retentionbedarf.

## Decision Logic

1. Ein Chat ist die normale Arbeitsoberfläche, aber nicht automatisch ein persistierter Capture. Bei eindeutigem Owner und belastbarem Delta wird direkt zum Owner propagiert.
2. Nur ungeklärten, aber erhaltenswerten Input als atomaren `capture` Record unter `inbox/captures/<uuid>.md` stagen.
3. Unverarbeitete Captures immer behalten.
4. Bei hohem Beweis-, Nuancen-, Wiederbeschaffungs- oder Auditrisiko Raw, Redaction oder stabilen Source Pointer erhalten.
5. Nach vollständiger Propagation normale Gedanken-Dumps verdichten, wenn kein materieller Verlust entsteht.
6. Nur ausdrücklich gewünschte, dauerhaft wertvolle oder mit konkretem Review-Trigger versehene Ideen als eigenen Record promoten. Der Record liegt bei genau einem fachlichen Owner in `identity`, `business`, `knowledge`, `finance`, `health` oder im `working`-Modul eines bereits existierenden Projects. Content-Ideen bleiben im ContentOS. Ist der Owner unklar, bleibt der Input Capture oder wird gezielt geklärt.
7. Chats nicht vollständig spiegeln; relevante, später nicht zuverlässig erreichbare Passagen gezielt persistieren.
8. Sensitive Inhalte minimieren und Secrets niemals in Captures übernehmen.

## Capture Record Contract

- `unprocessed`: Es hat noch keine vollständige Triage stattgefunden; der Originalinput bleibt verlustfrei erhalten und darf nicht gelöscht werden.
- `staged`: Die Triage ist abgeschlossen, aber ein konkret benanntes Owner-, Scope-, Bedeutungs- oder Reifegrad-Gate bleibt offen.
- `processed`: Propagation oder begründeter No-op, Retention und Verification sind vollständig abgeschlossen; Partial Failure bleibt `staged`.
- `processing_outcome`: `no-op`, `routed` oder `promoted`.
- `retention_disposition`: beschreibt den weiteren Umgang mit dem ursprünglichen Input als `raw-retained`, `redacted`, `stable-pointer`, `compacted` oder `discarded`, nicht die dauerhafte Aufbewahrung des Capture-Records.
- Materielle Outputs und No-op-Begründungen stehen im Body als Links; die Inbox wird dadurch nicht zur zweiten fachlichen Wahrheit.
- `processed` ist ein kurzlebiger Abschlusszustand innerhalb desselben Verarbeitungslaufs. Nach erfolgreichem Postflight wird der Capture-Record gelöscht. Erforderliche Raw Evidence oder Processing Receipts müssen davor bei ihrem kanonischen Source-, Interaction-, Automation- oder fachlichen Owner liegen; der Capture selbst wird nie zum dauerhaften Receipt.

## Idea Record Contract

- `idea` bezeichnet eine bewusst bewahrte Möglichkeit mit dauerhaftem Wert, aber noch ohne bestätigtes Commitment und ohne Project-Eintritt.
- Erlaubte Ownerpfade sind `<identity|business|knowledge|finance|health>/ideas/<uuid>.md` und `projects/<project>/working/ideas/<uuid>.md` für ausschließlich projectbezogene Ideen in einem bereits existierenden Project.
- `content/ideas/` gehört nicht zum allgemeinen Profile; Content-Ideen verwenden den aktiven ContentOS-Vertrag.
- `active` bedeutet bewusste Entwicklung. `parked` bedeutet dauerhafte Bewahrung ohne implizite Wiedervorlage. Für eine gewünschte spätere Neubewertung entsteht getrennt ein Attention Trigger.
- `terminal` benötigt den Outcome `promoted`, `merged` oder `rejected` und die dazu passende typisierte Auflösung: `promotion_ref`, `merge_target_ref` oder `rejection_evidence_refs`. Der knappe terminale Record bleibt als Provenance-Pointer erhalten.
- Eine mögliche spätere Initiative bleibt Idea beim fachlichen Owner, bis sie benannt, ausdrücklich verfolgt und koordinierte Arbeit für einen konkreten Outcome benötigt. Erst dann entsteht ein Project.

## Interfaces

- `inbox/` ist der globale Ingress für ungeklärten Input.
- Das Registry-Profile `capture` und [[system/templates/capture]] besitzen Pfad, Frontmatter und Body Shape des Staging-Records.
- Das Registry-Profile `idea` und [[system/templates/idea]] besitzen den verteilten, ownernahen Idea-Vertrag.
- [[system/frameworks/core/context-routing-and-truth-propagation]] besitzt Delta-, Maturity- und Owner-Routing.
- [[system/frameworks/operations/action-und-attention-modell]] übernimmt bestätigte Actions und Attention Trigger.
- Owning Skills dokumentieren Propagation oder begründeten No-op; sie erzeugen Receipts nur bei echtem Bedarf.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
