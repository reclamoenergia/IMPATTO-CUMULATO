# IMPATTO-CUMULATO (plugin QGIS)

Plugin QGIS per il calcolo del solo **VAI (Visual Angular Impact)** su DEM.

## Cosa calcola

Dato:
- layer punti turbine eoliche
- raster DEM
- raggio di analisi (metri)
- layer opzionale di recettori

il plugin calcola con logica LOS reale un solo indicatore:

- **VAI** in gradi²

Formula implementata:

- `VAI(P) = Σ (Aapp_vis_i * delta_theta_i)`

con:
- `Aapp_vis_i`: angolo verticale apparente della porzione visibile della turbina i
- `delta_theta_i`: ampiezza angolare orizzontale della turbina i

Il calcolo è fatto turbina per turbina e poi sommato. La visibilità usa l'orizzonte locale ottenuto campionando il DEM lungo la linea di vista osservatore→turbina.

Interpretazione sintetica:
- VAI misura l'impronta angolare visuale cumulata delle turbine visibili, combinando estensione verticale apparente e larghezza angolare orizzontale.

## Come avviare in QGIS

1. Abilita il plugin `IMPATTO-CUMULATO`.
2. Apri menu `IMPATTO-CUMULATO` → `IMPATTO-CUMULATO: VAI visibility`.
3. Nella finestra Processing imposta:
   - `Turbine points`
   - `Hub height field`
   - `Rotor diameter field`
   - `DEM raster`
   - `Analysis radius (m)`
   - `Output extent` (DEM oppure estensione turbine + buffer raggio)
   - `Output pixel size` (DEM oppure valore utente)
   - `Output folder`
   - `Output file prefix`
   - opzionale `Optional receptor points` e `Receptor VAI output`

## Output raster

Il plugin scrive un solo GeoTIFF georeferenziato:
- `<prefix>_VAI.tif`

NoData viene propagato dal DEM. Il raster valido viene aggiunto automaticamente al progetto QGIS.

## Output recettori opzionale

Se viene passato un layer recettori, il sink di output contiene i campi originali più:
- `vai`

`vai` è calcolato con la stessa logica LOS reale usata per il raster.
