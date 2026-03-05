# IMPATTO-CUMULATO (plugin QGIS)

Hai ragione: ora il plugin non mostra solo una demo, ma una **finestra di calcolo reale** dove inserire i componenti.

## Cosa trovi nel repository

- `calculator.py` → logica di calcolo dell'indice cumulato (media pesata + validazioni)
- `plugin.py` → UI QGIS con tabella componenti, calcolo e gestione errori
- `__init__.py` → entry-point richiesto da QGIS
- `metadata.txt` → metadati del plugin

## Funzionalità plugin

Dal menu plugin apri la finestra **IMPATTO-CUMULATO: calcolo** e puoi:

1. aggiungere/rimuovere righe componente;
2. impostare `nome`, `valore [0-1]`, `peso`;
3. calcolare l'indice cumulato con validazione input;
4. vedere subito il risultato nella stessa finestra.

## Installazione (git clone diretto nella cartella plugin)

> Usa la cartella `IMPATTO_CUMULATO` (underscore), così QGIS carica il plugin.

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
5. Apri dal menu: **IMPATTO-CUMULATO → IMPATTO-CUMULATO: calcolo**

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
