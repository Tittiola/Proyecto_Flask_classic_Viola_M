from registro_ig.models import *
import requests
from registro_ig.conexion import Conexion

from config import ORIGIN_DATA


registros = select_all()
lista_criptos=["ETH","BNB","ADA","DOT","BTC","USDT","XRP","SOL","MATIC"]

lista_crypto_verificada= []

for item in lista_criptos:
    if consulta_mon_from_to(item) == True:
        lista_crypto_verificada.append(item)

lista_crypto_from=[]
for item in lista_crypto_verificada:
    if consulta_mon_from(item)== True:
        lista_crypto_from.append(item)
#print(lista_crypto_from)

lista_crypto_to=[]
for item in lista_crypto_verificada:
    if consulta_mon_to(item)== True:
        lista_crypto_to.append(item)

lista_valor_actual_cada_crypto = []
for crypto in lista_crypto_verificada:
    cambio_in_euros= change_crypto(crypto)#per ogni cripto verificada hace cambio en euros
    if crypto in lista_crypto_to:
        recuperado=status_recuperado(crypto)[0][0]
    else: recuperado=0

    if crypto in lista_crypto_from:
            invertido=status_invertido(item)[0][0]
    else: invertido = 0

    cantidad_real_crypto = recuperado - invertido
    valoractualcrypto= (cambio_in_euros * cantidad_real_crypto)
    lista_valor_actual_cada_crypto.append(valoractualcrypto)
    resultado= sum(lista_valor_actual_cada_crypto)

print(resultado)


'''
        
        
        
    else:
        "error"


print(resultado)'''





'''lista_crypto_sum=[]

for crypto in lista_crypto_verificada:
   lista_crypto_sum.append(status_invertido(crypto)[0][0])

print(lista_crypto_sum)
    
list_n=[]


lista_crypto_from=[]
for item in lista_crypto_verificada:
    if consulta_mon_from(item)== True:
        lista_crypto_from.append(item)
print(lista_crypto_from)


lista_suma_crypto_from=[]
for item in lista_crypto_from:
    lista_suma_crypto_from += status_invertido(item)[0]'''

'''print(sum(lista_suma_crypto_from))



lista_crypto_to=[]
for item in lista_crypto_verificada:
    if consulta_mon_to(item)== True:
        lista_crypto_to.append(item)'''


'''lista_suma_crypto_to=[]
for item in lista_crypto_to:
    lista_suma_crypto_to += status_recuperado(item)[0]

print(sum(lista_suma_crypto_to))'''