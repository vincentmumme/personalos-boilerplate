# Warum PersonalOS existiert

## Der Ausgangspunkt

PersonalOS entstand aus Vincent Mummes täglicher Arbeit mit KI-Agenten. Je mehr Aufgaben Agenten übernehmen konnten, desto deutlicher wurde ein anderes Problem: Gute Ausführung hilft wenig, wenn der nötige Kontext in einzelnen Chats, Notizen, Tools und Köpfen verteilt ist.

Ein Agent konnte eine Aufgabe lösen und im nächsten Gespräch trotzdem wieder bei null anfangen. Entscheidungen blieben im Chat. Aufgaben lösten sich von ihrem Projektkontext. Externe Quellen wurden schnell zu vermeintlicher Wahrheit. Jeder neue Agent brauchte dieselben Erklärungen.

PersonalOS wurde als praktische Antwort auf diese Reibung aufgebaut: als lesbare Grundlage, die Menschen und unterschiedliche Agenten gemeinsam verwenden können.

## Die Grundidee

PersonalOS ist eine private Kontext- und Wahrheitsschicht auf Markdown-Basis. Es verbindet drei Dinge:

1. **Persönlichen und fachlichen Kontext:** Menschen, Unternehmen, Projekte, Entscheidungen, Wissen, Interaktionen und Tageskontext.
2. **Ausführung:** Aufgaben und Aufmerksamkeit liegen in einem klaren Operations-Bereich und bleiben mit ihrem Ursprung verknüpft.
3. **Systemlogik:** Regeln, Verträge, Frameworks, Templates, Runbooks und Checks bestimmen, wie ein Agent Informationen liest, einordnet, verändert und prüft.

Die Dateien sind nicht nur Speicher. Sie bilden ein Arbeitsmodell, das erklärt, was eine Quelle, ein Arbeitsstand, eine Entscheidung, eine aktuelle Wahrheit oder eine Aufgabe ist.

## Was Vincent damit verfolgt

Vincent baut PersonalOS nicht als starres Schema für jedes Leben. Das System soll einen belastbaren Anfang liefern und dann mit echter Nutzung wachsen. Es soll so simpel wie möglich bleiben und nur so viel Struktur erhalten, wie für eindeutige Zuständigkeit und verlässliche Agentenarbeit nötig ist.

Dabei gelten einige feste Leitplanken:

- Menschen bleiben die letzte Instanz für sensible und weitreichende Entscheidungen.
- Ein Agent darf Unsicherheit nicht als gesicherte Wahrheit behandeln.
- Persönliche Daten und Systemlogik bleiben getrennt.
- Aktuelle Wahrheit besitzt genau einen kanonischen Owner.
- Externe Systeme behalten ihre eigene Zuständigkeit, wenn sie dort besser aufgehoben ist.
- Automatisierung folgt einem verstandenen Ablauf. Sie ersetzt ihn nicht.
- Jede materielle Änderung braucht einen nachvollziehbaren Prüfpfad.

## Von Vincents System zur öffentlichen Boilerplate

Vincents privates PersonalOS bleibt das reale Referenzsystem. Darin liegen persönliche Records, Kundenkontext, konkrete Geräte, Accounts, Laufzeiten und aktive Automationen. Diese Inhalte gehören nicht in ein öffentliches Repository.

Die Boilerplate bildet das System trotzdem systematisch ab. Jede versionierte Quelldatei wird inventarisiert und als wiederverwendbarer Kern, neutralisierte Vorlage, optionales Modul, fiktives Beispiel oder bewusster Ausschluss klassifiziert. Neue unklassifizierte Dateien stoppen den Updateprozess.

So kann die öffentlich portable Systemlogik vollständig bereitgestellt werden, ohne Vincents private Instanz zu veröffentlichen. Der genaue Vertrag steht in [Produktvertrag](product-contract.md), die aktuelle Zuordnung in [Abdeckung und Reifegrad](coverage.md).

## Was du daraus machen kannst

Du kannst die Boilerplate vollständig installieren, nur passende Module auswählen, die Architektur zuerst verstehen oder einzelne Regeln und Templates übernehmen. Entscheidend ist nicht, dass dein PersonalOS genauso aussieht wie Vincents System. Entscheidend ist, dass dein Agent klare Quellen, Owner, Grenzen und Prüfwege vorfindet.

Der nächste sinnvolle Einstieg ist die [Karte des vollständigen Systems](system-map.md).
