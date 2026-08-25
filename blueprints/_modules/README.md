# Optionale Module

Module ergänzen den Pflichtkern um Lebensbereiche, Werkzeuge oder Infrastruktur. Kein Modul ist standardmäßig aktiv.

Jedes Modul beantwortet zwei Fragen:

- **So nutze ich es:** Welche Entscheidung hinter dem Referenzsystem steht und warum.
- **So kannst du es ausprobieren:** Welcher kleine, sichere Einstieg die Funktionsweise zeigt.

Ein Modul darf keine privaten Daten, Secrets, festen privaten Pfade oder aktive Zeitpläne enthalten. Tool- und Hostmodule dokumentieren Voraussetzungen und Grenzen. Ihre Payload ergänzt das installierte PersonalOS, ohne Regeln des Kerns zu überschreiben.

`catalog.json` listet alle verfügbaren Module. Der vollständige Ordner `reference/` entsteht aus dem Kern und allen Payloads.
