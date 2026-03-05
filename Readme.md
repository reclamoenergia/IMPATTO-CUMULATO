# QGIS Wind Visibility Plugin

Questo repository è preparato per essere pubblicato su GitHub senza errori legati a file binari.

## Cosa è stato sistemato

- Blocco dei file binari/artefatti non necessari con `.gitignore`.
- Regole `.gitattributes` per distinguere chiaramente file testuali e binari.
- Workflow consigliato per una **prima pubblicazione pulita** (senza merge manuali).

## Prima pubblicazione su GitHub (repo remoto vuoto)

> Usa questi comandi dalla cartella del progetto (`/workspace/IMPATTO-CUMULATO`).

```bash
git branch -M main
git remote add origin https://github.com/<TUO-UTENTE>/<TUO-REPO>.git
git push -u origin main
```

Se avevi già impostato `origin`:

```bash
git remote set-url origin https://github.com/<TUO-UTENTE>/<TUO-REPO>.git
git push -u origin main
```

## Aggiornamenti futuri (sempre senza merge manuale)

Con questo flusso lineare:

```bash
git add .
git commit -m "Messaggio"
git push
```

## Installazione plugin QGIS con **un unico comando**

### Linux (QGIS 3, profilo default)

```bash
git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO-CUMULATO
```

Poi apri QGIS e vai su **Plugin → Gestisci e installa plugin** per abilitarlo.

### Aggiornare il plugin già installato

```bash
git -C ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO-CUMULATO pull
```
