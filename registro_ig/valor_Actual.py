from registro_ig.models import *
ORIGIN_DATA="data/movimientos.sqlite"


registros = select_all()
lista_criptos=["ETH","BNB","ADA","DOT","BTC","USDT","XRP","SOL","MATIC"]

def valor_act():
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
        return resultado








