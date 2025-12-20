# Sistema di Tracciamento Alunni - ITS

Sistema di gestione e tracciamento degli studenti sviluppato per l'ITS.

# Requisiti

- Python 3.x
- Moduli standard: datetime, json, os, shutil, csv

# Installazione

1. Clona il repository
2. Assicurati di avere Python installato
3. Esegui il programma: python sistema_alunni_ITS.py

# Funzionalità

# Gestione Alunni
- **Inserisci nuovo alunno**: Registra studenti con nome, cognome, email e matricola univoca
- **Visualizza alunni**: Mostra tutti gli alunni registrati ed esporta in CSV
- **Modifica dati**: Aggiorna informazioni degli studenti
- **Elimina alunno**: Rimuovi studenti dal sistema

# Gestione Compiti
- **Assegna compito**: Crea nuovi compiti per gli studenti
- **Registra valutazione**: Segna i compiti come completati
- **Visualizza compiti**: Vedi tutti i compiti di uno studente

# Statistiche
- **Statistiche alunno**: Media voti, compiti assegnati/completati, progressione voti
- **Ranking**: Classifica studenti per media voti
- **Report compiti**: Lista compiti non ancora completati

# Persistenza Dati
- **Salva backup**: Backup dei dati in cartella dedicata
- **Carica dati**: Ripristina dati salvati

# Struttura File

- `sistema_alunni_ITS.py` - File principale
- `lista.json` - Dati alunni
- `listacompiti.json` - Dati compiti
- `report.csv` - Export CSV alunni
- `backup/` - Cartella backup

# Utilizzo

Avvia il programma e segui il menu interattivo. Digita la lettera corrispondente alla funzione desiderata (a-n).

# Esempio
```
Digita un comando: a
Nome: Mario
Cognome: Rossi
Email: Mario.Rossi@its.com
Matricola (premere invio per generare): 
✅ Alunno Mario Rossi inserito con successo!
```

# Note

- Le email devono seguire il formato: `nome.cognome@its.com`
- Le matricole vengono generate automaticamente in formato `MAT001`, `MAT002`, ecc.
- I voti devono essere compresi tra 0 e 10
- I dati vengono salvati automaticamente dopo ogni operazione

# Crediti
Progetto sviluppato per l'assignment ITS (Novembre 2025).
Ho usato Claude (AI di Anthropic) come assistente per:

- Aiuto nella gestione degli errori
- Debug e Testing in alcuni casi
- Organizazzione file README.md

