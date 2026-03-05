# QGIS Wind Visibility Plugin (IMPATTO-CUMULATO)

Hai ragione: prima mancavano i file sorgente del plugin. Ora il codice è incluso nel repository.

## Dove sta il codice

- `__init__.py` → entrypoint richiesto da QGIS (`classFactory`).
- `plugin.py` → classe principale del plugin (menu, toolbar, azione demo).
- `metadata.txt` → metadati richiesti da QGIS Plugin Manager.

## Struttura repository

```text
IMPATTO-CUMULATO/
├── __init__.py
├── plugin.py
├── metadata.txt
├── .gitattributes
├── .gitignore
└── Readme.md
```

## Prima pubblicazione su GitHub (repo remoto vuoto)

```bash
git branch -M main
git remote add origin https://github.com/<TUO-UTENTE>/<TUO-REPO>.git
git push -u origin main
```

Se `origin` esiste già:

```bash
git remote set-url origin https://github.com/<TUO-UTENTE>/<TUO-REPO>.git
git push -u origin main
```

## Flusso aggiornamenti (senza merge manuale)

```bash
git add .
git commit -m "Messaggio"
git push
```

## Installazione plugin QGIS con un unico comando

### Linux (QGIS 3, profilo default)

```bash
git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/impatto_cumulato
```

> Dopo il clone, in QGIS abilita il plugin da **Plugin → Gestisci e installa plugin**.

### Aggiornare plugin già installato

```bash
git -C ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/impatto_cumulato pull
```
