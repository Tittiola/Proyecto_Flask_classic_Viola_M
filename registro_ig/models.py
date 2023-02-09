import sqlite3
import requests
from registro_ig.conexion import Conexion

ORIGIN_DATA="data/movimientos.sqlite"
apiKey='336D91A9-5992-4CEE-A391-446D3AD7B024'


def change_from_to(moneda1, moneda2):
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{moneda1}/{moneda2}?apikey={apiKey}')
    #breakpoint()
    Q = consulta.json()
    return Q["rate"]



def change_crypto(moneda):
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{moneda}/EUR?apikey={apiKey}')

    Q = consulta.json()
    return Q["rate"]



def select_all():#importo todo lo que hay en el form sql a la pagina html
    connect = Conexion("select id,date,time,moneda_from,cantidad_from,moneda_to,cantidad_to from movements order by date;")
    columnas= connect.res.description#capturo los nombres de columnas
    filas = connect.res.fetchall()#capturo las filas de datos
    

    resultado= []#lista para guadar diccionario
   
    for fila in filas:
        dato={}#crear un diccionario para cada registro
        posicion=0#crear una posicion de columna para adjuntar y incrementar

        for campo in columnas:
            dato[campo[0]]=fila[posicion]#el campo columna es siempre en 0
            posicion += 1
        resultado.append(dato)

    connect.con.close()


    return resultado





def insert(registro):
    connectInsert = Conexion("insert into movements(date,time,moneda_from,cantidad_from,moneda_to,cantidad_to) values(?,?,?,?,?,?)", registro)
    connectInsert.con.commit()#funcion que registra finalmente
    connectInsert.con.close()

def consulta_mon_from(moneda):
    connectfind = Conexion("select moneda_from from movements where moneda_from == ?;", [moneda])
    resultado = connectfind.res.fetchall()
    if resultado == []:
        return False
    else:
       connectfind.con.close()
       return True 

def consulta_mon_to(moneda):
    connectfind = Conexion("select moneda_to from movements where moneda_to == ?;", [moneda])
    resultado = connectfind.res.fetchall()
    if resultado == []:
        return False
    else:
       connectfind.con.close()
       return True 

def consulta(registro):
    connectfind = Conexion("SELECT (moneda_from,moneda_to) from movements, values(?)",registro)
    resultado = connectfind.res.fetchall()
    connectfind.con.close()
    return resultado

def consulta_mon_from_to(moneda):
    moneda_is_in_mon_from = Conexion("select moneda_from from movements where cantidad_from > 0 and moneda_from == ?;", [moneda])
    resultado_from = moneda_is_in_mon_from.res.fetchall()
    moneda_is_in_mon_to = Conexion("select moneda_to from movements where cantidad_to  > 0 and moneda_to == ?;", [moneda])
    resultado_to = moneda_is_in_mon_to.res.fetchall()
    if resultado_from == [] and resultado_to == []:
        return False
    else:
       moneda_is_in_mon_to.con.close()
       moneda_is_in_mon_from.con.close()
       return True 

def delete_all():
    connectDelete = Conexion("DELETE FROM movements;")
    connectDelete.con.commit()
    connectDelete.con.close()
    connectre = Conexion("SELECT * from movements")
    connectre.con.commit()
    connectre.con.close()
    return select_all
    

def valor_compra(moneda):
    if consulta_mon_from(moneda) == False:
        invertido = 0
    else:
        invertido = status_invertido(moneda)[0][0]
    if consulta_mon_to(moneda) == False:
        recuperado= 0
    else:
        recuperado=status_recuperado(moneda)[0][0]
    valor_compra=invertido-recuperado
    return valor_compra


def status_invertido(moneda):  
    connectInvertido = Conexion("select sum(cantidad_from) from movements where moneda_from == ?;", [moneda])
    resultado =  connectInvertido.res.fetchall()
    connectInvertido.con.close()
    return resultado

def status_recuperado(moneda):  
    connectRecuperado = Conexion("select sum(cantidad_to) from movements where moneda_to == ?;", [moneda])
    resultado = connectRecuperado.res.fetchall()
    connectRecuperado.con.close()
    return resultado

def status_rec(moneda):  
    connectRecuperado = Conexion("select sum(cantidad_to) from movements where moneda_to == ?;", [moneda])
    resultado = connectRecuperado.res.fetchall()
    connectRecuperado.con.close()
    res = resultado(moneda)[0][0]
    return res

def valor_actua():
    lista_criptos=["ETH","BNB","ADA","DOT","BTC","USDT","XRP","SOL","MATIC"]

    lista_crypto_verificada= []
    for item in lista_criptos:
        if consulta_mon_from_to(item) == True:
            lista_crypto_verificada.append(item)

    lista_crypto_from=[]
    for item in lista_crypto_verificada:
        if consulta_mon_from(item)== True:
            lista_crypto_from.append(item)
    

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

    return(resultado)




