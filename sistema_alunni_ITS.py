from datetime import datetime
import json
import os
nummatricola=0
numerotask=0
lista=[]
listacomp=[]
lista_compiti=[]
listamatricole=[]
votomax=None
votomin=None
print("╔══════════════════════════════════════╗")
print("║ SISTEMA DI TRACCIAMENTO ALUNNI - ITS ║")
print("╚══════════════════════════════════════╝")


while True:
  scelta=input("""Seleziona un'opzione:
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
  n) Esci""").lower()

  if scelta=="a":
    print("╔════════════════════════╗")
    print("║ INSERISCI NUOVO ALUNNO ║")
    print("╚════════════════════════╝")

    nome=input("Nome : ")
    cognome=input("Cognome : ")
    email=input("Email : ")
    matricola=input("Matricola(premere invio per generare)")
    nummatricola=nummatricola+1
    if nummatricola<=9:
       print(f"MAT00{nummatricola}")
       numero=(f"MAT00{nummatricola}")
       listamatricole.append(numero)
       
    elif nummatricola<100:
        print(f"MAT0{nummatricola}")
        numero=(f"MAT00{nummatricola}")
        listamatricole.append(numero)
        
    else:
        print(f"MAT{nummatricola}")
        numero=(f"MAT00{nummatricola}")
        listamatricole.append(numero)
        
    print(f"Alunno {nome.capitalize()} {cognome.capitalize()} inserito con successo! ✅")
    oracreazione=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    oramodifica=oracreazione
    print(f"Data creazione:{oracreazione}")
    lista_alunni = {
    numero: {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "matricola": numero,
        "data_creazione": oracreazione,
        "data_modifica": oramodifica
    }}
    lista.append(lista_alunni)
    with open("lista.json","w")as file:
      json.dump(lista,file,indent=4)
    

  elif scelta=="b":
   print("╔══════════════════════════════╗")
   print("║ VISUALIZZA ALUNNI REGISTRATI ║")
   print("╚══════════════════════════════╝")
   if lista==[]:
        print("Ridigitare comando! 🛑 Nessun alunno registrato")
        with open("lista.json","w")as file:
            pass
   else:

    with open("lista.json","r")as file:
      lettura=json.load(file)
      for elementi in lettura:
         for chiave_esterna, dizionario_interno in elementi.items():
          print(f"--- {chiave_esterna} ---")
          for chiave_interna, valore_interno in dizionario_interno.items():
            print(f"  {chiave_interna}: {valore_interno}")
            

  elif scelta=="c":
    if lista==[]:
        print(" Non sono presenti alunni da modificare! Ridigitare comando! 🛑")
    else:
     print("╔══════════════════════╗")
     print("║ MODIFICA DATI ALUNNO ║")
     print("╚══════════════════════╝")
     numero=input("Inserire matricola a cui vorresti modificare i dati")
     datomodifica=input("Che dato vorresti modificare?").lower()
     modifica=input("inserisci modifica")
     lista_alunni[numero][datomodifica]=modifica
     oramodifica=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     print(f"Il dato dell'alunno con la matricola {numero} è stato modificato! ⚙️ ")

  elif scelta=="d":
    if lista==[]:
        print(" Non sono presenti alunni da eliminare! Ridigitare comando! 🛑")

    else:
      print("╔════════════════╗")
      print("║ ELIMINA ALUNNO ║")
      print("╚════════════════╝")
      numero=input("inserisci la matricola dell'alunno che vorresti eliminare")
      del lista_alunni[numero]
      print(f"L'alunno con la matricola {numero} è stato eliminato! 🗙")

  elif scelta=="e":
    if lista==[]:
        print("Non sono presenti alunni a cui assegnare compiti ! Ridigitare comando! 🛑")
    else:
     print("╔════════════════════════════╗")
     print("║ ASSEGNA COMPITO A STUDENTE ║")
     print("╚════════════════════════════╝")
     numerotask=numerotask+1
    if numerotask<=9:
       
       task=(f"TASK00{numerotask}")
       
    elif numerotask<100:
        
        task=(f"TASK00{numerotask}")
        
    else:
        
        task=(f"TASK00{numerotask}")

    while True:
        compitoalunno=input("scegli l'alunno a cui assegnare il compito:(inserire matricola alunno) ")
        if compitoalunno not in listamatricole:
            print("Matricola alunno non esistente! 🚨")
        else:
            break


    descrizione=input("Descrizione: ")
    print("Stato:assegnato")

    data_assegnazione=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    while True:
      voto=int(input("inserire voto"))
      if voto<0 or voto>10:
       raise ValueError("il voto deve essere compreso tra 0 e 10")
      else:
        break

    lista_compiti = {
    task: {
        "id": task,
        "descrizione": descrizione,
        "alunno_matricola": compitoalunno,
        "stato": "assegnato", 
        "data_assegnazione": data_assegnazione,
        "voto": voto
    }
    }
    print("Compito assegnato correttamente! ✅")
    listacomp.append(lista_compiti)

  elif scelta=="f":
     if lista==[]:
        print("Non ci sono alunni a cui registrare valutazioni. Ridigitare comando! 🛑")
     elif lista_compiti==[]:
        print("Non ci sono compiti da registrare. Ridigitare comando! 🛑")
     elif lista_compiti[task]["stato"]=="completato":
        print("Ridigitare comando! Valutazione già registrata🛑")

     else:
      print("╔══════════════════════╗")
      print("║ REGISTRA VALUTAZIONI ║")
      print("╚══════════════════════╝")
      lista_compiti[task]["stato"]="completato"
      lista_compiti[task]["voto"]="registrato"
      for chiave_esterna, dizionario_interno in lista_compiti.items():
        print(f"--- {chiave_esterna} ---")
        for chiave_interna, valore_interno in dizionario_interno.items():
            print(f"{chiave_interna} : {valore_interno}")


  elif scelta=="g":
    if lista==[]:
       print("Non sono presenti studenti a cui visualizzare i compiti. Ridigitare comando 🛑 ")
    elif lista_compiti==[]:
        print("Non ci sono compiti da visualizzare ! Ridigitare comando! 🛑")
    else:

     print("╔═══════════════════════════════════╗")
     print("║ VISUALIZZA COMPITI DEGLI STUDENTI ║")
     print("╚═══════════════════════════════════╝")
     lista_compiti[task]["voto"]=int(voto)

     for elementi in listacomp:
        for chiave_esterna, dizionario_interno in elementi.items():
         print(f"--- {chiave_esterna} ---")
         for chiave_interna, valore_interno in dizionario_interno.items():
            print(f"{chiave_interna} : {valore_interno}")

  elif scelta=="h":
     if lista==[]:
        print("Non sono presenti studenti a cui visualizzare le statistiche dei compiti ! Ridigitare comando! 🛑")
     elif lista_compiti==[]:
        print("Non sono presenti compiti di studenti. Ridigitare comando🛑")
     else:
        print("╔═══════════════════════════════╗")
        print("║ VISUALIZZA STATISTICHE ALUNNO ║")
        print("╚═══════════════════════════════╝")

        while True:
         statistichealunno=input("scegli l'alunno a cui visualizzare le statistiche :(inserire matricola alunno) ")
         if statistichealunno not in listamatricole:
            print("Matricola alunno non esistente! 🚨")
         else:
            break