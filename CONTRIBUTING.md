# Beitragen

Danke, dass du die PersonalOS Boilerplate verbessern möchtest.

## Geeignete Beiträge

- verständlichere Dokumentation und Beispiele,
- portable Regeln, Templates, Checks und Fähigkeiten,
- Fehlerbehebungen im Installer, Audit oder Exportmodell,
- Tests für reale Anwendungsfälle ohne persönliche Daten.

Persönliche PersonalOS-Inhalte, Kundenkontext, Zugangsdaten, private IDs, absolute private Pfade und aktive Account-Konfigurationen gehören nicht in dieses Repository.

## Ablauf

1. Eröffne bei größeren Änderungen zuerst ein GitHub Issue und beschreibe Problem, gewünschtes Ergebnis und Datenschutzgrenze.
2. Arbeite in einem Fork oder Feature-Branch.
3. Ergänze oder aktualisiere Tests bei Verhaltensänderungen.
4. Führe vor dem Pull Request die lokalen Prüfungen aus:

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
pos-boilerplate audit --build . --public-safe-terms policy/public-safe-terms.json
pos-boilerplate secret-scan --repository . --history
```

5. Beschreibe im Pull Request Wirkung, Grenzen und ausgeführte Prüfungen.

Die Pull-Request-Vorlage führt durch Ergebnis, Datenschutzgrenze und Verifikation. Kleine, klar abgegrenzte Pull Requests sind leichter zu prüfen als mehrere unabhängige Änderungen in einem Paket.

## Systemänderungen

Allgemeine PersonalOS-Systemlogik besitzt einen klaren Owner. Änderungen an Verträgen, Datenmodell, Templates oder Fähigkeiten müssen ihre Abhängigkeiten und Verifikation mitbringen. `reference/` wird aus `core/` und den Modul-Payloads erzeugt und nicht direkt gepflegt.

Mit einem Beitrag erklärst du dich damit einverstanden, ihn unter der MIT-Lizenz dieses Repositories bereitzustellen.
