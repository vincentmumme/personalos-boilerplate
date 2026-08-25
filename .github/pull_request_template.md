## Ergebnis

<!-- Was verbessert dieser Pull Request aus Sicht eines Nutzers? -->

## Umfang und Grenzen

<!-- Welche Bereiche ändern sich? Was bleibt bewusst unverändert? -->

## Datenschutz-Check

- [ ] Der Pull Request enthält keine persönlichen oder kundenspezifischen Inhalte.
- [ ] Er enthält keine Secrets, privaten IDs, absoluten privaten Pfade oder aktiven Account-Konfigurationen.
- [ ] Beispiele verwenden ausschließlich eindeutig fiktive Werte.
- [ ] Neue oder geänderte Quelldateien besitzen die erforderliche Exportklassifikation.

## Verifikation

- [ ] Relevante Tests wurden ergänzt oder bewusst als nicht erforderlich begründet.
- [ ] `python3 -m unittest discover -s tests -v`
- [ ] `pos-boilerplate audit --build . --public-safe-terms policy/public-safe-terms.json`
- [ ] `pos-boilerplate secret-scan --repository . --history`

<!-- Zusätzliche Prüfungen, Abweichungen oder bekannte Grenzen: -->
