# IMPATTO-CUMULATO (plugin QGIS)

Plugin QGIS per l'analisi cumulata di visibilità eolica su DEM.

## Cosa calcola

Dato:
- layer punti turbine eoliche
- raster DEM
- raggio di analisi (metri)
- layer opzionale di recettori

il plugin calcola con logica LOS reale:
- `Aapp_sum_vis` (somma angoli verticali apparenti visibili)
- `Hocc` (occupazione orizzonte in gradi, unione intervalli azimutali)
- `Dsky` (`Aapp_sum_vis / Hocc`)
- `ASTOR` (numero turbine visibili)

Le turbine sono visibili solo per la porzione sopra l'orizzonte locale derivato dal DEM campionato lungo la linea di vista.

## Come avviare in QGIS

1. Abilita il plugin `IMPATTO-CUMULATO`.
2. Apri menu `IMPATTO-CUMULATO` → `IMPATTO-CUMULATO: cumulative visibility`.
3. Nella finestra Processing imposta:
   - `Turbine points`
   - `Hub height field`
   - `Rotor diameter field`
   - `DEM raster`
   - `Analysis radius (m)`
   - `Output folder`
   - `Output file prefix`
   - opzionale `Optional receptor points` e `Receptor metrics output`

## Output raster

I raster sono scritti in GeoTIFF georeferenziati nella cartella scelta:
- `<prefix>_AappSumVis.tif`
- `<prefix>_Hocc.tif`
- `<prefix>_Dsky.tif`
- `<prefix>_ASTOR.tif`

NoData viene propagato dal DEM. I raster validi vengono aggiunti automaticamente al progetto QGIS.

## Output recettori opzionale

Se viene passato un layer recettori, il sink di output contiene:
- `n_vis`
- `d_min`
- `aapp_sum`
- `hocc`
- `dsky`
- `astor`

Tutti i valori sono calcolati con la stessa logica LOS reale usata per i raster.
