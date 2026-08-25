# Ableitungs- und Update-Modell

## Eine Richtung, keine zwei Wahrheiten

```text
privates PersonalOS
        |
        | kontrollierte Klassifikation und Neutralisierung
        v
PersonalOS Boilerplate
        |
        | Installation plus eigene Entscheidungen und eigener Kontext
        v
persönliche Instanz eines Nutzers
```

Die Boilerplate wird kontrolliert aus der privaten Referenzinstanz weiterentwickelt. Eine installierte Nutzerinstanz wird danach eigenständig. Updates dürfen ihre persönlichen Dateien nicht überschreiben.

## Klassifikationen

Jede Quelldatei erhält genau eine wirksame Behandlung:

- `copy`: unverändert wiederverwendbare Systemlogik
- `render`: Struktur wird übernommen, private oder instanzgebundene Inhalte werden durch universelle Inhalte ersetzt
- `module`: optionale Fähigkeit, die nicht zum Kern gehört
- `fixture`: Lernbeispiel, das ausschließlich mit fiktiven Daten erzeugt wird
- `exclude`: private Daten, Secrets, Laufzeitzustand oder bewusst nicht übertragbare Konfiguration

## Updateablauf

1. Quelldateien aus Git inventarisieren.
2. Jede Datei gegen die Policy klassifizieren.
3. Bei unklassifizierten Dateien abbrechen.
4. Kern und Module in einen frischen Staging-Ordner erzeugen.
5. Die vollständige Referenz aus Kern und allen Modulen zusammensetzen.
6. Datenschutz-, Link-, Schema- und Installationstests ausführen.
7. Unterschiede zur letzten Boilerplate-Version als Review-Diff zeigen.
8. Änderungen menschlich prüfen und erst danach übernehmen.
9. Release nach Semantic Versioning bewusst versionieren und veröffentlichen.

## Lokaler Maintainer Build

Die öffentliche Neutralisierung und die nicht versionierten privaten Ersetzungen werden getrennt geladen. Dadurch enthält das Repository keine geheimen Markerlisten, bleibt lokal aber deterministisch aus der Referenzinstanz aktualisierbar.

```bash
pos-boilerplate inventory \
  --source /path/to/private/PersonalOS \
  --policy policy/export-policy.json \
  --output reports/source-inventory.json

pos-boilerplate sync \
  --source /path/to/private/PersonalOS \
  --policy policy/export-policy.json \
  --output staging/current \
  --blueprints blueprints \
  --replacements policy/public-replacements.json \
  --replacements policy/replacements.local.json \
  --private-markers policy/private-markers.local.json \
  --public-safe-terms policy/public-safe-terms.json

pos-boilerplate audit \
  --build staging/current \
  --private-markers policy/private-markers.local.json \
  --public-safe-terms policy/public-safe-terms.json
```

Neue oder nicht klassifizierte Quelldateien stoppen den Build. Der erzeugte Staging-Stand wird erst nach Audit und Review in `core/`, `modules/`, `reference/` und `manifest.json` übernommen.

Der Sync darf niemals direkt auf das private PersonalOS oder auf dieses Git-Repository zeigen. Er ersetzt ausschließlich isolierte Build-Ordner, die sich durch eine gültige Boilerplate-Kennung, eine vollständige Dateiliste und passende Hashes als eigener Output ausweisen. Ein fremder Ordner, ein Git-Repository, ein Symlink oder ein veränderter Build wird abgelehnt.

`source_revision` und alle Quelldateien stammen immer aus demselben Commit. Noch nicht committete Änderungen oder ein abweichender Git-Index fließen nicht unbemerkt in eine öffentliche Ableitung ein. So bleibt jedes Update reproduzierbar und reviewbar.

## Umfang von Version 0.x

Der Maintainer aktualisiert die Boilerplate einseitig aus dem privaten Referenzsystem. Das Repository zeichnet Quell-Commit und Quelldatum im Manifest auf. Bereits personalisierte Nutzerinstanzen erhalten in dieser Version keinen automatischen Updater.

## Verhältnis zum Demo-POS

Das Demo-POS wird später aus derselben Boilerplate plus fiktiven Fixtures erzeugt. Es ist kein zweites, manuell gepflegtes System und kein Abbild privater Referenzdaten.
