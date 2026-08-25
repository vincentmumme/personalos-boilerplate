---
schema_version: pos-v1
id: 01a00149-b5ad-793d-9d70-a88f439d80eb
type: rule
title: "Timezone and Local Day Boundary"
created: 2026-08-14
updated: 2026-08-14
lifecycle: active
decision_refs: ["[[decisions/{{install_year}}/{{install_date}}-adopt-personalos-foundation]]"]
---

# Timezone and Local Day Boundary

## Rule

Jeder zeitgebundene POS-Write verwendet die fachlich maßgebliche lokale Zeitzone und bewahrt den tatsächlichen Zeitpunkt mit Offset. Weder Host-Lokalzeit noch ein historischer Instanz-Default dürfen die Tageszuordnung still bestimmen.

## Scope and Trigger

Die Rule gilt bei Day Records, Activity, Journal, Briefings, Interactions, Events, Automation Runs, Kalenderauswertung und allen Writes, deren Datum oder lokale Uhrzeit fachliche Bedeutung besitzt.

## Required Behavior

1. Eine explizit am Ereignis oder Auftrag angegebene IANA-Zeitzone hat Vorrang.
2. Fehlt sie, wird der bekannte Aufenthalts- oder Kalenderkontext für {{user_name}} beziehungsweise den fachlichen Ereignisowner verwendet.
3. Erst wenn beides fehlt, gilt der aktuelle Instanz-Default aus [[system/truth-systems/personalos]].
4. Exakte Zeitpunkte werden als RFC 3339 mit Sekunden und Offset gespeichert; lokale Tagesrecords speichern zusätzlich die IANA-Zeitzone.
5. Der lokale Kalendertag wird in dieser aufgelösten Zeitzone bestimmt.
6. Scheduled Automations deklarieren ihre gewünschte Schedule-Zeitzone unabhängig vom Host und werden bei einem bewussten Default-/Aufenthaltswechsel geprüft.
7. Historische Offsets, IANA-Zeitzonen und Day-Zuordnungen werden später nicht auf einen neuen Default umgeschrieben.

## Exceptions

Technische Vergleichs-, Transport- oder Providerzeit darf zusätzlich in UTC geführt werden. Sie ersetzt niemals die lokale persönliche oder fachliche Tagessemantik. Extern vorgegebene Zeitwerte bleiben quellennah erhalten und werden nur durch eine explizite normalisierte Interpretation ergänzt.

## Verification

- Aktive Writer lösen ihren Zeitkontext über `system/data-model/scripts/time_context.py` auf; der Instanz-Default darf nicht als zweite Konstante in Skills oder Auditcode dupliziert werden.
- Datetime-Felder müssen die Registry-Validierung für RFC 3339 mit Offset bestehen.
- Tagesgebundene Profile müssen Pfaddatum, `day_date` und `timezone` konsistent führen.
- Writer mit hartcodiertem `Europe/Berlin`, festen `+01:00`-/`+02:00`-Offsets oder impliziter Host-Lokalzeit sind rot, sofern diese Werte nicht explizit der aufgelöste aktuelle Kontext sind.
- Schedule- und Observability-Checks vergleichen gewünschten Automation-Kontext und gemessene Runtime, sobald der Scheduler die Zeitzone ausweist.

## Change History

- **{{install_date}}** | Foundation adopted from PersonalOS Boilerplate.
