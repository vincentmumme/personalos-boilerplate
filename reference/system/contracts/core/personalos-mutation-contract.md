---
schema_version: pos-v1
id: 019fec8b-0c08-7cad-b965-8bea69226e9e
type: contract
title: "PersonalOS Mutation Contract"
created: 2026-08-10
updated: 2026-08-11
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.1.0
---

# PersonalOS Mutation Contract

## Contract

Jede Erstellung, Änderung, Verschiebung, Löschung oder materielle Neufassung einer PersonalOS-Datei erfolgt direkt durch den spezifischen owning Skill oder einen ausdrücklich autorisierten Agenten innerhalb eines bekannten Owners, eines expliziten Write Scopes und eines definierten Verification-Pfads. Ein gesonderter `pos-write`-Skill ist dafür im Zielzustand weder Owner noch notwendiger Ausführungsschritt.

## Scope

Der Vertrag gilt für alle menschlichen und agentischen Writes im PersonalOS-Vault einschließlich Legacy-Records während des Cutovers, `pos-v1`-Records, Systemartefakte, Domainrecords, Interactions, Projects, Daily Records, Skills, Scripts, Moves und Deletes. Externe Systeme und Repositories folgen zusätzlich ihren eigenen Autorisierungs- und Transaktionsgrenzen.

## Invariants

- Intent, kanonischer Owner, zulässige Zielmenge und Mutationstyp sind vor dem Write bekannt.
- Neue Wahrheit besitzt eine Source-/Provenance-Basis und wird über eine Propagation Map gegen plausible angrenzende Owner geprüft.
- Ein owning Skill behält fachliche Entscheidungen; allgemeine Mutation Discipline verändert seine Domainautorität nicht.
- Neue `pos-v1`-Records werden ausschließlich aus einem writable Registry Profile und dessen kanonischem Template gerendert; IDs und Felder werden nicht improvisiert.
- Bestehende Records werden in ihrer aktuell autorisierten Shape bearbeitet, bis ihre Migrationswelle sie kontrolliert auf `pos-v1` umstellt.
- Current Truth wird bei State-Änderung neu synthetisiert; Timeline, Log, Source, Interaction oder Todo ersetzen keinen fachlichen Owner.
- Riskante, irreversible oder externe Veränderungen sowie materielle Identity-, Strategy-, Legal-, Finance- oder Communication-Writes benötigen die geltende Freigabe.
- Der Write bleibt auf die explizit ausgewählten Ziele begrenzt und erzeugt eine genaue Liste geänderter, verschobener oder gelöschter Dateien.
- Moves und Renames bewahren die Record-ID, folgen [[system/conventions/core/record-naming-and-temporal-paths]] und erfüllen [[system/contracts/core/internal-links-and-path-mutations]] einschließlich Inbound-Link-, Consumer- und Recovery-Nachweis.
- Partial Writes, Konflikte, ungeprüfte Targets und verbleibende Warnungen werden sichtbar berichtet.
- Jeder Write endet mit passender deterministischer und semantischer Verification.

## Interfaces

```text
Resolver oder direkter Intent
  -> owning Skill
  -> Context Routing and Truth Propagation
  -> Registry / Profile / Template
  -> Mutation
  -> PersonalOS Mutation Runbook
  -> PersonalOS Mutation Postflight
```

Der owning Skill referenziert die benötigten Systemnormen direkt. `system/data-model/scripts/pos_v1.py` rendert und validiert registrierte Records. [[system/runbooks/core/personalos-mutation]] operationalisiert diesen Contract. [[system/checks/core/personalos-mutation-postflight]] deklariert den Postflight; `pos-verify` bleibt während und nach dem Cutover die ausführbare semantische Verification-Capability.

Benennung und zeitliche Partitionierung werden durch [[system/conventions/core/record-naming-and-temporal-paths]] festgelegt. Pfadqualifizierte Wikilinks, ID-Stabilität, Linkrewrite, Redirects und Recovery bei Moves werden durch [[system/contracts/core/internal-links-and-path-mutations]] konkretisiert. Navigation und abgeleitete Sichten folgen [[system/conventions/core/index-view-and-discovery]].

## Compliance

Ein Write ist nicht compliant, wenn sein Owner unklar ist, ein erforderliches Profile oder Template fehlt, eine zweite aktuelle Wahrheit entsteht, Source/Provenance für materielle Claims fehlt, der Write Scope überschritten wird oder keine abschließende Verification stattfindet. Deterministische Checks ersetzen nicht die semantische Beurteilung, ob Wahrheit und Action beim richtigen Owner gelandet sind.

Während des Bootstrap-Cutovers darf `pos-write` als Compatibility-Adapter gelesen werden. Neue Normen werden dort nicht mehr aufgenommen. Der Skill wird retired, sobald Mutation Contract, Runbook, Checks, Resolver, Agenteneinstiege und mutierende Consumer grün umgestellt sind.

## Evolution

Neue Mutationstypen oder externe Transaction Boundaries erweitern den zuständigen Contract oder ein spezifisches Runbook. Domain-spezifische Freigaben und Write Scopes bleiben beim fachlichen Owner. Allgemeine Assertions werden als Rules, Contracts oder Checks unter `system/` ergänzt und nicht in mutierenden Skills dupliziert.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
