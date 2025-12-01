
lista=[]
while True:
    voto=int(input("inserisci voto"))
    
    if voto<10:
        numero=input("inserisci matricola")
     
        lista.append(numero)
        lista.append(voto)
    else:
        break

print(lista)

