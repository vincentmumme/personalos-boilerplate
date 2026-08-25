---
schema_version: pos-v1
id: 019ffc1a-c4f9-7302-8b22-ba77240c03a4
type: contract
title: "File and Asset Boundary"
created: 2026-08-13
updated: 2026-08-19
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
contract_version: 1.1.0
---

# File and Asset Boundary

## Contract

PersonalOS besitzt den Markdown-basierten Kontext und die nachvollziehbare Wahrheit über Dateien und Assets, aber nicht automatisch deren physische Binärdaten. Große, binäre, mutable oder gemeinsam auszutauschende Dateien liegen in einem ausdrücklich benannten Asset-System; PersonalOS hält den Owner, die Bedeutung, Provenance und einen auflösbaren Pointer oder ein Manifest.

## Scope

Der Vertrag gilt für PDFs, Bilder, Audio, Video, Archive, Office-Dateien, große Datensätze, Exporte, Renderings und andere Companion-Artefakte sowie für leichte maschinenlesbare Formate im Vault. Er entscheidet die Grenze zwischen Kontext- und Speicherwahrheit, nicht den noch offenen konkreten Aufbau von iCloud, Google Drive, NAS oder lokalen Asset-Roots.

## Invariants

- Markdown ist die primäre menschlich und agentisch lesbare Wahrheitsschicht.
- YAML, JSON, JSONL, CSV und andere leichte Companion-Formate sind nur mit klarem Owner, Zweck und Lifecycle zulässig.
- Große oder binäre Dateien werden nicht aus Bequemlichkeit in Git aufgenommen.
- Ein Asset-Pointer bezeichnet genau ein kanonisches Asset-System oder einen manifestierten Suchpfad; mehrere unmarkierte Kopien erzeugen keine zweite Wahrheit.
- Die fachliche Bedeutung eines Assets bleibt beim Domain- oder Project-Owner, nicht beim Speicheranbieter.
- Externe Austauschflächen wie Google Drive werden nur dann zum Asset-Owner, wenn dies für den konkreten Scope ausdrücklich festgelegt ist.
- Secrets, Kreditkartendaten und andere Zugangswerte sind keine Assets und folgen der Access-/Secret-Grenze.

## Interfaces

Project-, Content-, Finance-, Health-, Interaction- und andere Domainrecords dürfen Asset-Pointer oder Manifest-Relations halten. [[system/contracts/core/internal-links-and-path-mutations]] regelt interne POS-Links; [[system/contracts/system/system-topology-and-access]] regelt Access und Integrationen. Physische Moves benötigen ein Quell-/Zielinventar, Hash- oder Identitätsbeleg, Consumerplan und Recovery-Grenze.

## Compliance

Vor einem neuen Asset-Speicherpfad muss der zuständige Owner benannt sein. Unklare oder temporäre Dateien dürfen nicht durch einen neuen Root legitimiert werden. Ein Migration- oder Cleanup-Run klassifiziert jede Datei als extern zu bewahren, ownernah zu verschieben, als leichte Companion Data zu behalten oder kontrolliert zu löschen.

## Evolution

Die konkrete persönliche und kollaborative Datei-, Asset- und Recovery-Architektur wird in einer installationsspezifischen Architekturentscheidung entschieden. Sie darf diesen Grundvertrag erweitern, aber nicht den gesamten physischen Speicher zurück in PersonalOS ziehen oder POS-Kontext durch providerabhängige Ordner ersetzen. Die universelle Verweislogik bleibt speicherübergreifend; konkrete Ordnerstrukturen werden später je tatsächlich verwendetem Speicherort definiert.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
