# Sistema tracciamento alunni - ITS
from datetime import datetime
import json
import os
import shutil
import csv

# VARIABILI GLOBALI 

# Contatori per generare ID univoci
contatore_matricole = 0
contatore_task = 0

# Liste principali
lista_alunni = []  # Lista con tutti gli alunni registrati
lista_tutti_compiti = []  # Lista con tutti i compiti assegnati
lista_matricole_esistenti = []  # Lista delle matricole già usate

# Liste per statistiche
lista_voti_alunni = []  # Lista con i voti di ogni alunno
lista_compiti_assegnati = []  # Lista con numero compiti assegnati per alunno
lista_compiti_completati = []  # Lista con numero compiti completati per alunno

# Cartella per backup
nome_cartella_backup = "backup"

#  FUNZIONI 

def inserisci_alunno():
    """Funzione per inserire un nuovo alunno nel sistema"""
    global contatore_matricole
    
    print("╔════════════════════════╗")
    print("║ INSERISCI NUOVO ALUNNO ║")
    print("╚════════════════════════╝")
    
    # Richiesta dati alunno
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    
    # Validazione email con controllo formato
    while True:
        email = input("Email: ").strip()
        if email != f"{nome}.{cognome}@its.com":
            print("❌ Email non valida! Deve essere: nome.cognome@its.com")
        else:
            break
    
    # Generazione matricola univoca automatica
    input("Matricola (premere invio per generare): ")
    contatore_matricole += 1
    
    # Ciclo per trovare una matricola non usata
    while True:
        # Formattazione matricola con zeri iniziali
        if contatore_matricole <= 9:
            numero_matricola = f"MAT00{contatore_matricole}"
        elif contatore_matricole < 100:
            numero_matricola = f"MAT0{contatore_matricole}"
        else:
            numero_matricola = f"MAT{contatore_matricole}"
        
        # Controlla se la matricola è già stata usata
        if numero_matricola not in lista_matricole_esistenti:
            lista_matricole_esistenti.append(numero_matricola)
            break
        else:
            contatore_matricole += 1
    
    print(f"Matricola assegnata: {numero_matricola}")
    print(f"✅ Alunno {nome.capitalize()} {cognome.capitalize()} inserito con successo!")
    
    # Timestamp creazione
    ora_creazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Data creazione: {ora_creazione}")
    
    # Creazione dizionario alunno
    dati_alunno = {
        numero_matricola: {
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "matricola": numero_matricola,
            "data_creazione": ora_creazione,
            "data_modifica": ora_creazione
        }
    }
    lista_alunni.append(dati_alunno)
    salva_alunni()

def visualizza_alunni():
    """Funzione per visualizzare tutti gli alunni registrati"""
    print("╔══════════════════════════════╗")
    print("║ VISUALIZZA ALUNNI REGISTRATI ║")
    print("╚══════════════════════════════╝")
    
    # Controlla se ci sono alunni registrati
    if not lista_alunni:
        print("🛑 Nessun alunno registrato")
        return
    
    # Stampa informazioni di ogni alunno
    for alunno in lista_alunni:
        for matricola, dati in alunno.items():
            print(f"\n--- {matricola} ---")
            for campo, valore in dati.items():
                print(f"  {campo}: {valore}")
    
    # Esportazione CSV
    dati_per_csv = []
    for alunno in lista_alunni:
        for matricola, dati in alunno.items():
            riga = [
                dati["matricola"],
                dati["nome"],
                dati["cognome"],
                dati["email"]
            ]
            dati_per_csv.append(riga)
    
    try:
        # Scrittura file CSV 
        with open('report.csv', 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerow(["Matricola", "Nome", "Cognome", "Email"])
            writer.writerows(dati_per_csv)
        print("\n📄 Report CSV generato con successo!")
    except Exception as errore:
        print(f"⚠️ Errore durante la creazione del CSV: {errore}")

def modifica_alunno():
    """Funzione per modificare i dati di un alunno esistente"""
    print("╔══════════════════════╗")
    print("║ MODIFICA DATI ALUNNO ║")
    print("╚══════════════════════╝")
    
    # Controlla se ci sono alunni da modificare
    if not lista_alunni:
        print("🛑 Non sono presenti alunni da modificare!")
        return
    
    # Richiesta matricola alunno
    while True:
        matricola_da_modificare = input("Inserire matricola dell'alunno: ").strip()
        if matricola_da_modificare not in lista_matricole_esistenti:
            print("🚨 Matricola alunno non esistente!")
        else:
            break
    
    # Richiesta campo da modificare
    while True:
        campo_da_modificare = input("Che dato vorresti modificare? (nome/cognome/email): ").lower().strip()
        if campo_da_modificare not in ["nome", "cognome", "email"]:
            print("⚠️  Campo non valido! Riprova.")
        else:
            break
    
    nuova_modifica = input("Inserisci la modifica: ").strip()
    
    # Aggiornamento timestamp modifica
    ora_modifica = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Cerca e modifica l'alunno nella lista
    for alunno in lista_alunni:
        if matricola_da_modificare in alunno:
            alunno[matricola_da_modificare][campo_da_modificare] = nuova_modifica
            alunno[matricola_da_modificare]["data_modifica"] = ora_modifica
    
    print(f"⚙️ Il dato dell'alunno con matricola {matricola_da_modificare} è stato modificato!")
    salva_alunni()

def elimina_alunno():
    """Funzione per eliminare un alunno dal sistema"""
    print("╔════════════════╗")
    print("║ ELIMINA ALUNNO ║")
    print("╚════════════════╝")
    
    # Controlla se ci sono alunni da eliminare
    if not lista_alunni:
        print("🛑 Non sono presenti alunni da eliminare!")
        return
    
    # Richiesta matricola alunno da eliminare
    while True:
        matricola_da_eliminare = input("Inserire matricola da eliminare: ").strip()
        if matricola_da_eliminare not in lista_matricole_esistenti:
            print("🚨 Matricola alunno non esistente!")
        else:
            break
    
    # Trova l'indice dell'alunno da rimuovere
    for indice, alunno in enumerate(lista_alunni):
        if matricola_da_eliminare in alunno:
            indice_da_rimuovere = indice
            break
    
    # Rimozione alunno dalla lista
    del lista_alunni[indice_da_rimuovere]
    lista_matricole_esistenti.remove(matricola_da_eliminare)
    
    print(f"🗙 L'alunno con matricola {matricola_da_eliminare} è stato eliminato!")
    salva_alunni()

def assegna_compito():
    """Funzione per assegnare un compito a uno studente"""
    global contatore_task
    
    print("╔════════════════════════════╗")
    print("║ ASSEGNA COMPITO A STUDENTE ║")
    print("╚════════════════════════════╝")
    
    # Controlla se ci sono alunni a cui assegnare compiti
    if not lista_alunni:
        print("🛑 Non sono presenti alunni a cui assegnare compiti!")
        return
    
    # Generazione ID task univoco
    contatore_task += 1
    
    if contatore_task <= 9:
        id_task = f"TASK00{contatore_task}"
    elif contatore_task < 100:
        id_task = f"TASK0{contatore_task}"
    else:
        id_task = f"TASK{contatore_task}"
    
    # Richiesta matricola studente
    while True:
        matricola_studente = input("Matricola alunno: ").strip()
        if matricola_studente not in lista_matricole_esistenti:
            print("🚨 Matricola alunno non esistente!")
        else:
            break
    
    # Richiesta descrizione compito
    descrizione_compito = input("Descrizione compito: ").strip()
    print("Stato: assegnato")
    
    # Timestamp assegnazione
    data_assegnazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Richiesta voto 
    while True:
        try:
            voto_input = input("Inserire voto (0-10): ")
            voto = float(voto_input)
            if voto < 0 or voto > 10:
                print("⚠️  Il voto deve essere compreso tra 0 e 10!")
            else:
                break
        except ValueError:
            print("⚠️  Inserire un numero valido!")
    
    # Salvataggio voto per statistiche
    dati_voto = {
        matricola_studente: {
            "voto": voto
        }
    }
    lista_voti_alunni.append(dati_voto)
    
    # Salvataggio compito assegnato per statistiche
    compito_assegnato = {
        matricola_studente: {
            "compiti_assegnati": 1
        }
    }
    lista_compiti_assegnati.append(compito_assegnato)
    
    # Creazione dizionario compito
    dati_compito = {
        id_task: {
            "id": id_task,
            "descrizione": descrizione_compito,
            "alunno_matricola": matricola_studente,
            "stato": "assegnato",
            "data_assegnazione": data_assegnazione,
            "voto": voto
        }
    }
    
    lista_tutti_compiti.append(dati_compito)
    print("✅ Compito assegnato correttamente!")
    salva_compiti()

def registra_valutazione():
    """Funzione per registrare una valutazione di un compito"""
    print("╔══════════════════════╗")
    print("║ REGISTRA VALUTAZIONE ║")
    print("╚══════════════════════╝")
    
    # Controlla se ci sono alunni e compiti
    if not lista_alunni:
        print("🛑 Non ci sono alunni registrati!")
        return
    
    if not lista_tutti_compiti:
        print("🛑 Non ci sono compiti da registrare!")
        return
    
    # Richiesta ID task da registrare
    while True:
     id_task_da_registrare = input("Inserire ID Task da registrare: ").strip()
    
     task_trovato = False
     # Cerca il task e cambia lo stato
     for compito in lista_tutti_compiti:
        if id_task_da_registrare in compito:
            compito[id_task_da_registrare]["stato"] = "registrato"
            matricola_studente = compito[id_task_da_registrare]["alunno_matricola"]
            
            # Salvataggio compito completato per statistiche
            compito_completato = {
                matricola_studente: {
                    "compiti_completati": 1
                }
            }
            lista_compiti_completati.append(compito_completato)
            task_trovato = True
            print("✅ Valutazione registrata con successo!")
            break
    
     if task_trovato:
            break
     else:
            print("🚨 Task non trovato! Riprova.")
    
    salva_compiti()

def visualizza_compiti_studente():
    """Funzione per visualizzare tutti i compiti di uno studente"""
    print("╔════════════════════════════════════╗")
    print("║ VISUALIZZA COMPITI DI UNO STUDENTE ║")
    print("╚════════════════════════════════════╝")
    
    # Controlla se ci sono studenti e compiti
    if not lista_alunni:
        print("🛑 Non sono presenti studenti!")
        return
    
    if not lista_tutti_compiti:
        print("🛑 Non ci sono compiti da visualizzare!")
        return
    
    # Richiesta matricola studente
    while True:
        matricola_studente = input("Inserire matricola alunno: ").strip()
        if matricola_studente not in lista_matricole_esistenti:
            print("🚨 Matricola alunno non esistente!")
        else:
            break
    
    # Cerca e stampa tutti i compiti dello studente
    compiti_trovati = False
    for compito in lista_tutti_compiti:
        for id_task, dati in compito.items():
            if compito[id_task]["alunno_matricola"] == matricola_studente:
                print(f"\n--- {id_task} ---")
                for campo, valore in dati.items():
                    print(f"  {campo}: {valore}")
                compiti_trovati = True
    
    if not compiti_trovati:
        print("✋🏻 Nessun compito trovato per questo studente")

def visualizza_statistiche():
    """Funzione per visualizzare le statistiche complete di un alunno"""
    print("╔═══════════════════════════════╗")
    print("║ VISUALIZZA STATISTICHE ALUNNO ║")
    print("╚═══════════════════════════════╝")
    
    # Controlla se ci sono studenti e compiti
    if not lista_alunni:
        print("🛑 Non sono presenti studenti!")
        return
    
    if not lista_tutti_compiti:
        print("🛑 Non sono presenti compiti!")
        return
    
    # Richiesta matricola studente
    while True:
        matricola_studente = input("Inserire matricola alunno: ").strip()
        if matricola_studente not in lista_matricole_esistenti:
            print("🚨 Matricola alunno non esistente!")
        else:
            break
    
    # Raccolta di tutti i voti dello studente
    lista_voti = []
    for voti in lista_voti_alunni:
        for matricola, dati in voti.items():
            if matricola == matricola_studente:
                for campo, valore in dati.items():
                    lista_voti.append(valore)
    
    # Controlla se ci sono voti
    if not lista_voti:
        print("✋🏻  Nessun voto disponibile per questo studente")
        return
    
    # Calcolo statistiche voti 
    try:
        somma_voti = sum(lista_voti)
        numero_voti = len(lista_voti)
        media_voti = somma_voti / numero_voti
        voto_massimo = max(lista_voti)
        voto_minimo = min(lista_voti)
    except Exception as errore:
        print(f"⚠️  Errore nel calcolo statistiche: {errore}")
        return
    
    print(f"\n--- {matricola_studente} ---")
    print(f"📊 Media voti: {media_voti:.2f}")
    
    # Calcolo numero compiti assegnati
    lista_num_assegnati = []
    for compiti in lista_compiti_assegnati:
        for matricola, dati in compiti.items():
            if matricola == matricola_studente:
                for campo, valore in dati.items():
                    lista_num_assegnati.append(valore)
    
    totale_assegnati = sum(lista_num_assegnati) if lista_num_assegnati else 0
    print(f"📝 Numero compiti assegnati: {totale_assegnati}")
    
    # Calcolo numero compiti completati
    lista_num_completati = []
    for compiti in lista_compiti_completati:
        for matricola, dati in compiti.items():
            if matricola == matricola_studente:
                for campo, valore in dati.items():
                    lista_num_completati.append(valore)
    
    totale_completati = sum(lista_num_completati) if lista_num_completati else 0
    print(f"✅ Numero compiti completati: {totale_completati}")
    print(f"⬆️ Voto massimo: {voto_massimo}")
    print(f"⬇️ Voto minimo: {voto_minimo}")
    
    # Progressione voti nel tempo
    print("\n📈 Progressione voti nel tempo:")
    for numero, voto in enumerate(lista_voti, 1):
        print(f"  Voto {numero}: {voto}")

def ranking_alunni():
    """Funzione per visualizzare il ranking degli alunni per media voti"""
    print("╔═══════════════════════════════╗")
    print("║ RANKING ALUNNI PER MEDIA VOTI ║")
    print("╚═══════════════════════════════╝")
    
    # Controlla se ci sono studenti e compiti
    if not lista_alunni:
        print("🛑 Non sono presenti studenti!")
        return
    
    if not lista_tutti_compiti:
        print("🛑 Non sono presenti compiti!")
        return
    
    # Dizionario per salvare le medie di ogni studente
    dizionario_medie = {}
    
    # Calcola la media per ogni matricola
    for matricola in lista_matricole_esistenti:
        lista_voti_temp = []
        for voti in lista_voti_alunni:
            for matr, dati in voti.items():
                if matr == matricola:
                    for campo, valore in dati.items():
                        lista_voti_temp.append(valore)
        
        # Se lo studente ha voti, calcola la media 
        if lista_voti_temp:
            try:
                somma = sum(lista_voti_temp)
                numero = len(lista_voti_temp)
                media = somma / numero
                dizionario_medie[matricola] = media
            except Exception:
                continue
    
    # Controlla se ci sono medie da mostrare
    if not dizionario_medie:
        print("✋🏻  Nessun dato disponibile per il ranking")
        return
    
    # Ordina il dizionario per media (dal più alto al più basso)
    dizionario_ordinato = dict(sorted(dizionario_medie.items(), key=lambda x: x[1], reverse=True))
    
    # Stampa il ranking
    print("\n🏆 CLASSIFICA:")
    for posizione, (matricola, media) in enumerate(dizionario_ordinato.items(), 1):
        print(f"{posizione}. {matricola}: {media:.2f}")

def report_compiti_non_completati():
    """Funzione per visualizzare tutti i compiti non ancora completati"""
    print("╔═══════════════════════════════╗")
    print("║ REPORT COMPITI NON COMPLETATI ║")
    print("╚═══════════════════════════════╝")
    
    # Controlla se ci sono studenti e compiti
    if not lista_alunni:
        print("🛑 Non sono presenti studenti!")
        return
    
    if not lista_tutti_compiti:
        print("🛑 Non sono presenti compiti!")
        return
    
    # Cerca compiti non registrati
    compiti_non_completati_trovati = False
    for compito in lista_tutti_compiti:
        for id_task, dati in compito.items():
            if compito[id_task]["stato"] != "registrato":
                if not compiti_non_completati_trovati:
                    print("\n⚠️ Compiti non completati:")
                    compiti_non_completati_trovati = True
                print(f"\n--- {id_task} ---")
                for campo, valore in dati.items():
                    print(f"  {campo}: {valore}")
    
    if not compiti_non_completati_trovati:
        print("✅ Tutti i compiti sono stati completati!")

def salva_backup():
    """Funzione per salvare i dati in una cartella di backup"""
    print("╔════════════════════╗")
    print("║ SALVA DATI(BACKUP) ║")
    print("╚════════════════════╝")
    
    try:
        # Crea la cartella se non esiste
        if not os.path.exists(nome_cartella_backup):
            os.makedirs(nome_cartella_backup)
            print(f"📁 Cartella '{nome_cartella_backup}' creata")
        
        # Percorsi di destinazione
        percorso_backup_alunni = os.path.join(nome_cartella_backup, "lista.json")
        percorso_backup_compiti = os.path.join(nome_cartella_backup, "listacompiti.json")
        
        # Copia i file nella cartella backup
        if os.path.exists("lista.json"):
            shutil.copy("lista.json", percorso_backup_alunni)
        if os.path.exists("listacompiti.json"):
            shutil.copy("listacompiti.json", percorso_backup_compiti)
        
        print("✅ Backup completato con successo!")
    except Exception as errore:
        print(f"⚠️ Errore durante il backup: {errore}")

def carica_dati():
    """Funzione per caricare i dati salvati dai file JSON"""
    global contatore_matricole, contatore_task
    
    print("╔══════════════╗")
    print("║ CARICA DATI  ║")
    print("╚══════════════╝")
    
    try:
        # Caricamento dati alunni
        if os.path.exists("lista.json"):
            with open("lista.json", "r") as file:
                dati_caricati = json.load(file)
                for alunno in dati_caricati:
                    if alunno not in lista_alunni:
                        lista_alunni.append(alunno)
                    for matricola in alunno.keys():
                        if matricola not in lista_matricole_esistenti:
                            lista_matricole_esistenti.append(matricola)
                            # Aggiorna il contatore matricole
                            numero = int(matricola.replace("MAT", ""))
                            if numero > contatore_matricole:
                                contatore_matricole = numero
            print("✅ Dati alunni caricati")
        else:
            print("✋🏻  Nessun file di alunni trovato")
        
        # Caricamento dati compiti
        if os.path.exists("listacompiti.json"):
            with open("listacompiti.json", "r") as file:
                dati_caricati = json.load(file)
                for compito in dati_caricati:
                    if compito not in lista_tutti_compiti:
                        lista_tutti_compiti.append(compito)
                    for id_task, dati in compito.items():
                        # Aggiorna il contatore task
                        numero = int(id_task.replace("TASK", ""))
                        if numero > contatore_task:
                            contatore_task = numero
                        
                        # Ricostruisce le liste per statistiche
                        dati_voto = {
                            compito[id_task]["alunno_matricola"]: {
                                "voto": compito[id_task]["voto"]
                            }
                        }
                        lista_voti_alunni.append(dati_voto)
                        
                        compito_assegnato = {
                            compito[id_task]["alunno_matricola"]: {
                                "compiti_assegnati": 1
                            }
                        }
                        lista_compiti_assegnati.append(compito_assegnato)
                        
                        # Se il compito è registrato, aggiunge ai completati
                        if compito[id_task]["stato"] == "registrato":
                            compito_completato = {
                                compito[id_task]["alunno_matricola"]: {
                                    "compiti_completati": 1
                                }
                            }
                            lista_compiti_completati.append(compito_completato)
            print("✅ Dati compiti caricati")
        else:
            print("✋🏻  Nessun file di compiti trovato")
    
    except Exception as errore:
        print(f"⚠️ Errore durante il caricamento: {errore}")

def salva_alunni():
    """Salva la lista alunni nel file JSON"""
    try:
        with open("lista.json", "w") as file:
            json.dump(lista_alunni, file, indent=4)
    except Exception as errore:
        print(f"⚠️ Errore nel salvataggio alunni: {errore}")

def salva_compiti():
    """Salva la lista compiti nel file JSON"""
    try:
        with open("listacompiti.json", "w") as file:
            json.dump(lista_tutti_compiti, file, indent=4)
    except Exception as errore:
        print(f"⚠️ Errore nel salvataggio compiti: {errore}")

def mostra_menu():
    """Mostra il menu principale con tutte le opzioni disponibili"""
    
    print("""
Seleziona un'opzione:
  a) Inserisci nuovo alunno
  b) Visualizza alunni registrati
  c) Modifica dati alunno
  d) Elimina alunno
  e) Assegna compito a studente
  f) Registra valutazione
  g) Visualizza compiti di uno studente
  h) Visualizza statistiche alunno
  i) Ranking alunni per media voti
  j) Report compiti non completati
  k) Salva dati (backup)
  l) Carica dati
  m) Visualizza menu
  n) Esci""")

# PROGRAMMA PRINCIPALE

def main():
    """Funzione principale del programma"""
    print("╔══════════════════════════════════════╗")
    print("║ SISTEMA DI TRACCIAMENTO ALUNNI - ITS ║")
    print("╚══════════════════════════════════════╝")
    print("""
Seleziona un'opzione:
  a) Inserisci nuovo alunno
  b) Visualizza alunni registrati
  c) Modifica dati alunno
  d) Elimina alunno
  e) Assegna compito a studente
  f) Registra valutazione
  g) Visualizza compiti di uno studente
  h) Visualizza statistiche alunno
  i) Ranking alunni per media voti
  j) Report compiti non completati
  k) Salva dati (backup)
  l) Carica dati
  m) Visualizza menu
  n) Esci""")
    
    # Ciclo principale del programma
    while True:
        scelta = input("\nDigita un comando: ").lower().strip()
        
        # Esegue la funzione corrispondente alla scelta
        if scelta == "a":
            inserisci_alunno()
        
        elif scelta == "b":
            visualizza_alunni()
        
        elif scelta == "c":
            modifica_alunno()
        
        elif scelta == "d":
            elimina_alunno()
        
        elif scelta == "e":
            assegna_compito()
        
        elif scelta == "f":
            registra_valutazione()
        
        elif scelta == "g":
            visualizza_compiti_studente()
        
        elif scelta == "h":
            visualizza_statistiche()
        
        elif scelta == "i":
            ranking_alunni()
        
        elif scelta == "j":
            report_compiti_non_completati()
        
        elif scelta == "k":
            salva_backup()
        
        elif scelta == "l":
            carica_dati()
        
        elif scelta == "m":
            mostra_menu()
        
        elif scelta == "n":
            print("\n👋 Arrivederci!")
            break
        
        else:
            print("⚠️ Comando non valido! Digita 'm' per il menu")

# Esegue il programma solo se questo file viene eseguito direttamente
if __name__ == "__main__":
    main()