---
schema_version: pos-v1
id: 019fec98-2572-7e94-9203-88f4a70ef680
type: check
title: "Capability Control Plane Integrity"
created: 2026-08-10
updated: 2026-08-10
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
system_refs: ["[[system/contracts/core/capability-interface]]", "[[system/contracts/normative-system-architecture]]"]
check_kind: health
verifies_refs: ["[[system/contracts/core/capability-interface]]", "[[system/contracts/normative-system-architecture]]"]
---

# Capability Control Plane Integrity

## Purpose

Dieser Check stellt sicher, dass der Skill Resolver und die registrierten Capability-Schnittstellen erreichbar, eindeutig und mit dem Systemvertrag vereinbar bleiben.

## Assertions

- Der zentrale Resolver-Check existiert und ist ausführbar.
- Resolver-Einträge verweisen auf vorhandene Skills und erzeugen keine blockierenden Mehrdeutigkeiten.
- Retired Skills und ihre historischen Routing Fixtures werden nicht als aktive Resolver-/Index-Consumer verlangt; aktive Links auf retired Skills bleiben unzulässig.
- Registrierte Capability-I/O-Profile, Templates, Skills und Checks sind auflösbar.
- Skills mit POS-Record-Writes deklarieren ihre Write-Profile und Verification Owner; externe Seiteneffekte werden nicht als POS-Write fehlklassifiziert.

## Implementation

`system/checks/system/scripts/check-resolvable.py` prüft die bestehende Resolver-Fläche und unterscheidet aktive von retired Skills. `system/checks/system/scripts/test_check_resolvable.py` sichert die Retire-Grenze. Registry Validation besitzt die Capability-I/O-Typen und Relations. `pos-verify` aggregiert deren Exit Status, ohne Resolver- oder Capability-Semantik neu zu definieren.

## Invocation

```bash
python3 system/checks/system/scripts/check-resolvable.py
python3 system/data-model/scripts/pos_v1.py --root . check-registry
```

## Outcomes

- `pass`: Resolver und registrierte Capability-Schnittstellen sind konsistent.
- `warn`: ein ausdrücklich zugelassener Legacy-Target ist noch nicht migriert.
- `fail`: Resolver, registrierter Target oder mutierender Capability-Vertrag ist nicht auflösbar.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
