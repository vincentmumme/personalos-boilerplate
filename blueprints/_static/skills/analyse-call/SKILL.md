---
name: analyse-call
description: "Use this when a local call transcript or meeting note should be analyzed into traceable PersonalOS context. Preserves the source, separates evidence from interpretation, updates only proven owner truth, routes confirmed commitments through task-manager, and never sends messages or triggers external actions without explicit approval."
metadata:
  pos_schema_version: pos-v1
  pos_id: 01a02fb3-6e1d-720d-ac40-b8060fd8a5da
  pos_type: skill
  pos_title: "Skill: analyse-call"
  pos_created: "2026-08-23"
  pos_updated: "2026-08-23"
  pos_lifecycle: active
  pos_skill_version: 1.0.0
  pos_system_refs: ["[[system/contracts/core/capability-interface]]", "[[system/contracts/core/personalos-mutation-contract]]", "[[system/frameworks/interactions/signal-evidence-und-processing]]", "[[system/frameworks/core/context-routing-and-truth-propagation]]"]
  pos_reads_profile_keys: ["interaction-event", "source-evidence", "person", "company", "project", "action"]
  pos_writes_profile_keys: ["interaction-event", "interaction-analysis", "person", "company", "project", "action"]
  pos_template_refs: ["[[system/templates/interactions/interaction-event]]", "[[system/templates/interactions/source-evidence]]", "[[system/templates/interactions/interaction-analysis]]", "[[system/templates/action]]"]
  pos_invokes_skill_refs: ["[[skills/task-manager/SKILL]]", "[[skills/pos-verify/SKILL]]"]
  pos_check_refs: ["[[system/checks/pos-v1-contract]]", "[[system/checks/core/personalos-mutation-postflight]]"]
---

# Skill: analyse-call

## Contract

Dieser Skill überführt einen bereits lokal vorliegenden Call nachvollziehbar in PersonalOS-Kontext.

- Der Transkriptauszug oder die Meeting-Notiz bleibt als `source-evidence` erhalten.
- Das Gespräch, seine Interpretation und die daraus übernommene aktuelle Wahrheit bleiben drei unterscheidbare Ebenen.
- Nur Aussagen, die der Beleg wirklich trägt, verändern Person, Company oder Projekt.
- Unsicherheit und ausdrückliche Nichtentscheidungen bleiben sichtbar.
- Bestätigte nächste Handlungen werden ausschließlich über [[skills/task-manager/SKILL|task-manager]] als Actions geführt.
- Eine Action erlaubt noch keine Nachricht, Einladung, Kalenderänderung oder andere externe Ausführung.
- Jede Änderung endet mit [[skills/pos-verify/SKILL|pos-verify]] auf der ausdrücklichen Dateiliste.

## Ablauf

### 1. Quelle und Grenze lesen

Lies das Interaction Event und jede verknüpfte Evidence-Datei vollständig. Halte fest, was die Quelle belegt, was sie nicht belegt und ob der Inhalt real, anonymisiert oder fiktiv ist. Verändere Evidence nicht, um sie an die spätere Interpretation anzupassen.

### 2. Betroffenen Kontext laden

Lies nur die verknüpften oder eindeutig betroffenen Personen, Companies, Projekte, Actions und Systemregeln. Kläre vor dem Schreiben:

- Was gilt bereits?
- Was ist im Call wirklich neu?
- Welche Aussage ersetzt oder präzisiert bisherigen Stand?
- Welche offenen Punkte bleiben offen?
- Welche bestätigte Handlung gehört in Operations?

### 3. Analyse vor Propagation schreiben

Erstelle unter `analysis/<uuid>.md` eine `interaction-analysis` nach [[system/templates/interactions/interaction-analysis]]. Trenne Findings, Unsicherheit, Propagation und Quellen. Eine plausible Interpretation wird nicht allein dadurch zu Current Truth.

### 4. Kanonische Owner gezielt aktualisieren

Ändere nur die Abschnitte, deren aktueller Stand sich wirklich geändert hat. Formuliere Current Truth neu und gegenwartsbezogen, statt einen weiteren datierten Absatz anzuhängen. Geschichte und Belege bleiben in Timeline, Interaction und Evidence. Lege keine parallele Wahrheit in der Analyse an.

### 5. Commitments mit task-manager abgleichen

Suche zuerst nach einer bestehenden passenden Action. Erstelle nur bei einer eindeutig bestätigten Verpflichtung eine neue Action. Ohne bestätigten Owner oder klaren nächsten Schritt bleibt ein Punkt Open Question oder No-op. Führe keine externe Handlung aus.

### 6. Prüfen und sichtbar übergeben

Führe `python3 skills/pos-verify/scripts/run.py --files <geänderte Dateien>` aus. Berichte danach kompakt:

- welcher Beleg verarbeitet wurde
- welche Analyse entstand
- welche Owner sich materiell änderten
- welche Action erstellt oder bewusst nicht erstellt wurde
- welche Unsicherheit oder Freigabegrenze bleibt
- ob die Prüfung bestanden wurde

## Grenzen

- Keine automatische Recherche und keine Verknüpfung externer Konten.
- Keine erfundenen Teilnehmer, Entscheidungen, Fristen, Prioritäten oder Zusagen.
- Keine Rohtranskripte in Person, Company oder Projekt kopieren.
- Keine vertraulichen Daten in Suchanfragen oder externe Werkzeuge übertragen.
- Keine externen Nachrichten, Einladungen, Kalenderänderungen oder Automationen ohne ausdrückliche Freigabe.

## Change History

- **2026-08-23** | Öffentliche, lokale Kernfähigkeit für nachvollziehbare Call-Analyse angelegt.
