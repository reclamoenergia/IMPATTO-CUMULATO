# IMPATTO-CUMULATO (plugin QGIS)

Hai ragione: adesso nel repository c'è anche il **codice del plugin**.

## Dove sta il codice

- `calculator.py` → funzioni di calcolo dell'indice cumulato
- `plugin.py` → integrazione QGIS (menu + azione demo)
- `__init__.py` → entry-point richiesto da QGIS
- `metadata.txt` → metadati del plugin

## Installazione (git clone diretto nella cartella plugin)

> Usa il nome cartella `IMPATTO_CUMULATO` (con underscore), così QGIS lo carica correttamente.

### Linux

```bash
git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO_CUMULATO
```

### Windows (PowerShell)

```powershell
git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\IMPATTO_CUMULATO"
```

### macOS

```bash
git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO_CUMULATO
```

## Abilitazione in QGIS

1. Apri QGIS
2. Plugin → Gestisci e installa plugin
3. Cerca `IMPATTO-CUMULATO`
4. Abilita il plugin

## Aggiornamento

### Linux

```bash
git -C ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO_CUMULATO pull
```

### Windows

```powershell
git -C "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\IMPATTO_CUMULATO" pull
```

### macOS

```bash
git -C ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO_CUMULATO pull
```

## Nota sul calcolo

La funzione principale è `compute_cumulative_impact(...)` in `calculator.py`.
Calcola la media pesata dei componenti normalizzati in `[0,1]` e valida i dati in input.
