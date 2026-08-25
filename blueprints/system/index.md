---
schema_version: pos-v1
id: "{{id_system_index}}"
type: owner-index
title: "System"
created: "{{install_date}}"
updated: "{{install_date}}"
index_scope: root
---

# System

## Purpose

`system/` besitzt die allgemeine PersonalOS-Systemlogik. Persönliche und fachliche Wahrheit liegt außerhalb dieses Ordners bei ihren jeweiligen Ownern.

## Ownership and Boundaries

Systemregeln werden hier gepflegt, nicht in Skills dupliziert. Hosts, Runtimes, Integrationen, Services und Automationen werden erst als optionale Instanzmodule angelegt, wenn sie wirklich existieren.

## Navigation

- [[system/contracts/index]] – verbindliche Grenzen und Verantwortung
- [[system/conventions/index]] – Benennung, Records und Navigation
- [[system/frameworks/index]] – Denk- und Arbeitsmodelle
- [[system/frameworks/core/glossar]] – interne und technische Begriffe in klarer Sprache
- [[system/principles/index]] – stabile Systemprinzipien
- [[system/rules/index]] – verbindliche Regeln
- [[system/data-model/index]] – Profile, Felder und Validierung
- [[system/templates/index]] – kanonische Record-Vorlagen
- [[system/runbooks/index]] – sichere Änderungsabläufe
- [[system/checks/index]] – Zustands- und Integritätsprüfungen

## Maintenance

- Neue Systemkategorien entstehen nur durch eine bewusste Governance-Entscheidung.
- Normen werden beim zuständigen Owner geändert und danach gegen Registry, Links und betroffene Consumer geprüft.
