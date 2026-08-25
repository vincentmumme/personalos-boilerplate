---
schema_version: pos-v1
id: 019fec98-2518-78df-9df3-6d1329054021
type: framework
title: "Verification Ownership"
created: 2026-08-10
updated: 2026-08-13
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Verification Ownership

## Purpose

Das Framework ordnet jede PersonalOS-Prüfung ihrem normativen Ursprung, deklarativen Check-Owner und ausführenden Mechanismus zu. Damit kann `pos-verify` schrittweise dünner werden, ohne Assertions zu verlieren oder neue unsichtbare Normen im Code zu erzeugen.

## Model

```text
Norm / Profile
    -> deklarativer Check-Owner
        -> ausführbarer Checker
            -> Finding Code
                -> pass | warn | fail
```

Normen definieren das Soll. Check-Records bündeln die zugehörigen Assertions. Code führt sie deterministisch aus. Skills orchestrieren die Prüfung und beurteilen semantische Fragen, besitzen aber weder die Norm noch das Record-Shape.

## Components

| Verification Area | Deklarativer Owner | Ausführung | Finding-Familien |
|---|---|---|---|
| Write Scope und Dateisicherheit | [[system/checks/core/personalos-mutation-postflight]] | `skills/pos-verify/scripts/run.py` | `no_changed_files`, `large_git_discovery`, `missing_or_deleted_file`, `conflict_marker` |
| Markdown- und Linkintegrität | [[system/checks/core/markdown-record-integrity]] | `skills/pos-verify/scripts/run.py` | `missing_frontmatter`, `noncanonical_yaml_list`, `broken_wikilink`, `ambiguous_wikilink`, `pos_v1_internal_markdown_link` |
| `pos-v1` Registry Contract | [[system/checks/pos-v1-contract]] | `system/data-model/scripts/pos_v1.py` plus Adapter | `pos_v1_runtime_missing`, `pos_v1_registry_error`, `pos_v1_generated_drift` sowie Registry-Findings |
| Capability Control Plane | [[system/checks/system/capability-control-plane-integrity]] | `system/checks/system/scripts/check-resolvable.py` plus Adapter | `check_resolvable_missing`, `check_resolvable_failed` |
| Legacy Compatibility | [[system/checks/migration/pos-gbrain-v1-compatibility]] | befristete Funktionen in `skills/pos-verify/scripts/run.py` | `canonical_not_v1`, Current-Truth-/Timeline-, `v1_*`- und Legacy-Skill-Findings |
| Semantisches Routing und Propagation | [[system/checks/core/personalos-mutation-postflight]] | owning Skill plus dünner `pos-verify`-Skill | semantischer Befund im Verification-Ergebnis |

Die vollständige maschinenlesbare Zuordnung aller statisch emittierten Finding Codes liegt in `system/checks/core/verification-ownership.json` und wird gegen den Runner getestet.

## Decision Logic

1. Eine neue Assertion beginnt bei einer bestehenden Rule, einem Contract, Framework oder Registry Profile.
2. Gibt es keinen passenden Check-Owner, wird ein `check`-Record geschaffen, bevor Code die Assertion blockierend erzwingt.
3. Ein generischer Checker liest Registry oder Check-Konfiguration; er dupliziert keine Feld- oder Body-Semantik.
4. Ein profilspezifischer Checker gehört zum Profile-Admission-Paket und muss beim Profile-Cutover grün sein.
5. Legacy-Assertions werden ausdrücklich als Compatibility klassifiziert und mit Retire-Bedingung versehen.
6. Neue Profile müssen in der generischen Verification berücksichtigt werden; stille Coverage-Lücken sind blockierend.
7. Semantische Owner-, Provenance- und Propagation-Fragen bleiben Agentenprüfung, bis ein deterministischer Vertrag möglich ist.

## Interfaces

- Skills referenzieren ihre ausführbaren Check-Owner über `check_refs`.
- Checks referenzieren die verifizierten Normen über `verifies_refs` und direkte Abhängigkeiten über `system_refs`.
- Registry Validation prüft Struktur, Felder, Sections, Pfade und deklarierte Relations.
- `pos-verify` aggregiert Ergebnisse für eine explizite Write-Menge und ergänzt die semantische Prüfung.
- Das Ownership-JSON verbindet Finding Code und kanonischen Check-Pfad ohne eine zweite Norm zu definieren.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
