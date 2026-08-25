---
schema_version: pos-v1
id: 019ffbfe-fa55-7242-9e1e-f201af0040d5
type: contract
title: "System Topology and Access"
created: 2026-08-13
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.0.0
---

# System Topology and Access

## Contract

`system/` besitzt die kanonische Meta-Wahrheit über Agenten, agentenspezifische Persona-Overlays, Runtimes, Hosts, Services, Integrationen, Access-Identitäten, Operating Systems und abgeleitete Observability. Jeder reale Bestandteil erhält genau einen typisierten Record; Beziehungen werden über stabile Wikilinks modelliert.

## Scope

Der Vertrag gilt für alle aktuellen und geplanten Agenten-Setups, Geräte, VPS-/Cloud-Hosts, lokale oder geplante Services, CLI-/API-/SSH-Zugriffe, externe Integrationen und XOS-Kontexte, die PersonalOS verwenden oder beeinflussen. Er gilt nicht für fachliche Domain Truth, Tasks, Run-Evidence, Repository-Implementierung oder Secret-Werte.

## Invariants

1. Root-`SOUL.md` ist die gemeinsame Grundseele; agentenspezifische Overlays ergänzen sie sichtbar und dürfen gemeinsame Systemverträge nicht aufheben.
2. Agent, Runtime und Host sind getrennte Objekte: Verhalten, Ausführungsumgebung und physischer beziehungsweise virtueller Rechner werden nicht vermischt.
3. Ein Service beschreibt gewünschten Betrieb und Ausführungsziel; beobachteter Zustand bleibt eine abgeleitete Observability View.
4. Integrationen beschreiben externe Grenzen und Datenaustausch, nicht fachliche Wahrheit des externen Systems.
5. Access-Records enthalten benötigte Identitäten, Accounts, CLI-Authorizations, SSH-Zugriffe und sichere Pointer, niemals Secret-Werte.
6. 1Password ist aktueller Owner der Secret-Werte. Synchronisierte `.env` und lokale Runtime-Umgebungen bleiben ausdrücklich dokumentierte Übergangsmechanismen, keine Zielarchitektur für Multi-Person-/VPS-Provisionierung.
7. Automations besitzen Cadence und Run-Receipts; ein paralleler Scheduler-Truth-Root entsteht nicht.

## Interfaces

- Agent-Records verlinken Persona, Scope und zuständige Runtimes/Hosts im Body.
- Runtime-Records besitzen typisierte `agent_refs` und `host_refs`.
- Host-Records dokumentieren ihre technische Plattform in `Operating System`. Die XOS-Registry unter `system/operating-systems/` bleibt semantisch getrennt und beschreibt PersonalOS, ContentOS, BusinessOS und verwandte Systemmodule, nicht macOS, Linux oder Windows.
- Service-Records verlinken Runtime oder Host sowie optional ihre Integration.
- Access-Records verlinken jeden Agenten, Runtime, Host, Service oder jede Integration, die den Zugang benötigt.
- Observability Views leiten Soll/Ist-Zustand aus diesen Ownern und technischen Snapshots ab.

## Compliance

Zehn registrierte Profile, zentrale Templates, positive und negative Fixtures, Registry-Schemas und der Check [[system/checks/system/system-topology-integrity]] erzwingen Shape, Relationen und Secret-Grenze. Legacy-Cutovers benötigen Source-Hash, Disposition, Writer-/Consumerplan, Recovery und den Nachweis, dass kein alter Writer mehr auf den entfernten Pfad schreibt.

## Evolution

Neue Topologieklassen werden nur aufgenommen, wenn sie nicht als Agent, Persona-Overlay, Runtime, Host, Service, Integration, Access, Operating System oder abgeleitete View modellierbar sind. Zukünftige VPS-, BOS- und Multi-Person-Secret-Provisionierung ist eine eigene Richtungsentscheidung und ändert den heutigen Pointer-Vertrag nicht automatisch.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
