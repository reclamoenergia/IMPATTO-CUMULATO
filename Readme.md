# IMPATTO-CUMULATO (plugin QGIS)

Plugin QGIS per l'analisi cumulata di visibilità eolica su DEM.

## Cosa calcola

Dato:
- layer punti turbine eoliche
- raster DEM
- raggio di analisi (metri)
- layer opzionale di recettori

il plugin calcola con logica LOS reale:
- `Aapp_sum`: somma degli angoli verticali apparenti delle porzioni visibili
- `Hocc`: occupazione orizzontale del profilo in gradi (unione intervalli azimutali)
- `VAI`: Visual Angular Impact in gradi², definito come `Σ(Aapp_vis_i * delta_theta_i)`

Dove:
- `Aapp_sum(P) = Σ Aapp_vis_i`
- `Hocc(P)` è la lunghezza totale dell'unione degli intervalli azimutali occupati
- `VAI(P) = Σ (Aapp_vis_i * delta_theta_i)`

Interpretazione sintetica:
- `Aapp_sum` misura la dominanza visiva verticale cumulata
- `Hocc` misura l'occupazione orizzontale del skyline
- `VAI` misura l'impronta angolare visuale cumulata

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
   - `Output extent` (DEM oppure estensione turbine + buffer raggio)
   - `Output pixel size` (DEM oppure valore utente)
   - `Output folder`
   - `Output file prefix`
   - opzionale `Optional receptor points` e `Receptor metrics output`

## Output raster

I raster sono scritti in GeoTIFF georeferenziati nella cartella scelta:
- `<prefix>_AappSum.tif`
- `<prefix>_Hocc.tif`
- `<prefix>_VAI.tif`

NoData viene propagato dal DEM. I raster validi vengono aggiunti automaticamente al progetto QGIS.

## Output recettori opzionale

Se viene passato un layer recettori, il sink di output contiene i campi originali più:
- `aapp_sum`
- `hocc`
- `vai`

Tutti i valori sono calcolati con la stessa logica LOS reale usata per i raster.
