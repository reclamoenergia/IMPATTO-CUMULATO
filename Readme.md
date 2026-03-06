diff --git a/Readme.md b/Readme.md
index 5948b02f8c8a17d355ef4d254db347953aa27e02..395561037b77bf37b8695d6cd537e3fdb3a5ffd3 100644
--- a/Readme.md
+++ b/Readme.md
@@ -1,52 +1,69 @@
-# QGIS Wind Visibility Plugin
+# IMPATTO-CUMULATO (plugin QGIS)
 
-Questo repository è preparato per essere pubblicato su GitHub senza errori legati a file binari.
+Hai ragione: ora il plugin non mostra solo una demo, ma una **finestra di calcolo reale** dove inserire i componenti.
 
-## Cosa è stato sistemato
+## Cosa trovi nel repository
 
-- Blocco dei file binari/artefatti non necessari con `.gitignore`.
-- Regole `.gitattributes` per distinguere chiaramente file testuali e binari.
-- Workflow consigliato per una **prima pubblicazione pulita** (senza merge manuali).
+- `calculator.py` → logica di calcolo dell'indice cumulato (media pesata + validazioni)
+- `plugin.py` → UI QGIS con tabella componenti, calcolo e gestione errori
+- `__init__.py` → entry-point richiesto da QGIS
+- `metadata.txt` → metadati del plugin
 
-## Prima pubblicazione su GitHub (repo remoto vuoto)
+## Funzionalità plugin
 
-> Usa questi comandi dalla cartella del progetto (`/workspace/IMPATTO-CUMULATO`).
+Dal menu plugin apri la finestra **IMPATTO-CUMULATO: calcolo** e puoi:
 
-```bash
-git branch -M main
-git remote add origin https://github.com/<TUO-UTENTE>/<TUO-REPO>.git
-git push -u origin main
-```
+1. aggiungere/rimuovere righe componente;
+2. impostare `nome`, `valore [0-1]`, `peso`;
+3. calcolare l'indice cumulato con validazione input;
+4. vedere subito il risultato nella stessa finestra.
+
+## Installazione (git clone diretto nella cartella plugin)
 
-Se avevi già impostato `origin`:
+> Usa la cartella `IMPATTO_CUMULATO` (underscore), così QGIS carica il plugin.
+
+### Linux
 
 ```bash
-git remote set-url origin https://github.com/<TUO-UTENTE>/<TUO-REPO>.git
-git push -u origin main
+git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO_CUMULATO
 ```
 
-## Aggiornamenti futuri (sempre senza merge manuale)
+### Windows (PowerShell)
+
+```powershell
+git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\IMPATTO_CUMULATO"
+```
 
-Con questo flusso lineare:
+### macOS
 
 ```bash
-git add .
-git commit -m "Messaggio"
-git push
+git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO_CUMULATO
 ```
 
-## Installazione plugin QGIS con **un unico comando**
+## Abilitazione in QGIS
+
+1. Apri QGIS
+2. Plugin → Gestisci e installa plugin
+3. Cerca `IMPATTO-CUMULATO`
+4. Abilita il plugin
+5. Apri dal menu: **IMPATTO-CUMULATO → IMPATTO-CUMULATO: calcolo**
+
+## Aggiornamento
 
-### Linux (QGIS 3, profilo default)
+### Linux
 
 ```bash
-git clone https://github.com/<TUO-UTENTE>/<TUO-REPO>.git ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO-CUMULATO
+git -C ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO_CUMULATO pull
 ```
 
-Poi apri QGIS e vai su **Plugin → Gestisci e installa plugin** per abilitarlo.
+### Windows
+
+```powershell
+git -C "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\IMPATTO_CUMULATO" pull
+```
 
-### Aggiornare il plugin già installato
+### macOS
 
 ```bash
-git -C ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO-CUMULATO pull
+git -C ~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins/IMPATTO_CUMULATO pull
 ```
