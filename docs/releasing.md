# Release-Prozess

Dieser Ablauf richtet sich an Maintainer mit Zugriff auf die private Referenzinstanz. Öffentliche Nutzer benötigen weder die private Quelle noch lokale Markerdateien.

## 1. Referenzstand festlegen

Der private PersonalOS-Stand muss committed sein. Nicht commitete Änderungen werden vom Generator bewusst nicht übernommen. Die neue `source_revision` im Manifest muss dem freigegebenen Commit entsprechen.

## 2. Vollständigkeit prüfen und isoliert bauen

```bash
python3 -m pip install -e .

pos-boilerplate inventory \
  --source /path/to/private/PersonalOS \
  --policy policy/export-policy.json \
  --output reports/source-inventory.json

pos-boilerplate sync \
  --source /path/to/private/PersonalOS \
  --policy policy/export-policy.json \
  --output /path/to/new/isolated-build \
  --blueprints blueprints \
  --replacements policy/public-replacements.json \
  --replacements policy/replacements.local.json \
  --private-markers policy/private-markers.local.json \
  --public-safe-terms policy/public-safe-terms.json
```

Der Output muss ein neuer, leerer Pfad außerhalb der privaten Referenzinstanz und außerhalb dieses Git-Repositories sein. Unterschiede werden menschlich geprüft. Erst danach werden `core/`, `modules/`, `reference/` und `manifest.json` aus dem geprüften Build übernommen.

## 3. Release-Gates

Das Repository-Secret `POS_PRIVATE_MARKERS_JSON` enthält die lokale Markerliste als JSON-Array. Der Job `Protected privacy markers` läuft vor dem Merge über `pull_request_target`. Er installiert den Scanner ausschließlich aus dem vertrauenswürdigen Hauptzweig, lädt den Pull Request nur als Git-Daten und führt keinen Code daraus aus. Die Markerliste wird außerhalb des Repository-Ordners materialisiert. Der Job muss in der Branch Protection als erforderlicher Statuscheck eingetragen sein.

Direkte Pushes auf den Hauptzweig müssen gesperrt sein. Die lokale Release-Prüfung bleibt zusätzlich vor Tag und Veröffentlichung verpflichtend:

```bash
POS_RELEASE_AUDIT=1 python3 -m unittest discover -s tests -v

pos-boilerplate audit \
  --build . \
  --private-markers policy/private-markers.local.json \
  --public-safe-terms policy/public-safe-terms.json

pos-boilerplate secret-scan \
  --repository . \
  --history \
  --private-markers policy/private-markers.local.json \
  --public-safe-terms policy/public-safe-terms.json
```

Zusätzlich wird die Installation in einem neuen Zielordner ausgeführt und der Einstieg aus Sicht eines Nutzers geprüft, der keinen Zugriff auf die private Referenzinstanz besitzt.

## 4. Öffentliche Freigabe

1. Release-Diff, Changelog, Version und Lizenz prüfen.
2. GitHub Issues aktivieren.
3. CI auf dem Release-Commit abwarten.
4. Version `v0.1.0` taggen und einen GitHub-Release als Entwurf vorbereiten.
5. Repository öffentlich schalten.
6. Unmittelbar danach **Security → Private vulnerability reporting** aktivieren. GitHub stellt diese Funktion erst für öffentliche Repositories bereit.
7. Repository-Link ausgeloggt öffnen und Schnellstart, Lizenz, Issues sowie **Security → Report a vulnerability** prüfen.
8. Den vorbereiteten GitHub-Release veröffentlichen.
9. Erst danach den Link in externen Kanälen teilen.

Die öffentliche GitHub-Freigabe und externe Kommunikation benötigen eine bewusste Maintainer-Freigabe.
