import sqlite3
import requests
from registro_ig.conexion import Conexion

ORIGIN_DATA="data/movimientos.sqlite"
apiKey='24E07BC2-CA11-4FD2-9F14-889CEE3B8DBF'

#funciones con peticiones api
def change_from_to(moneda1, moneda2):#funcion que devuelve el cambio poniendo dos tipos de monedas
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{moneda1}/{moneda2}?apikey={apiKey}')
    #breakpoint()
    Q = consulta.json()
    return Q["rate"]

def change_crypto(moneda):#funcion que pide el cambio en Euros poniendo un tipo de crypto
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{moneda}/EUR?apikey={apiKey}')

    Q = consulta.json()
    return Q["rate"]

#funciones con peticiones sqlite

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



def insert(registro):#funcion que permite registrar datos en form sqlite
    connectInsert = Conexion("insert into movements(date,time,moneda_from,cantidad_from,moneda_to,cantidad_to) values(?,?,?,?,?,?)", registro)
    connectInsert.con.commit()#funcion que registra finalmente
    connectInsert.con.close()

def consulta_mon_from(moneda):#funcion que consulta si una moneda esta en moneda_from, para no devolver NoType y devolver en su lugar True o False
    connectfind = Conexion("select moneda_from from movements where moneda_from == ?;", [moneda])
    resultado = connectfind.res.fetchall()
    if resultado == []:
        return False
    else:
       connectfind.con.close()
       return True 

def consulta_mon_to(moneda):#funcion que consulta si una moneda esta en moneda_to, para no devolver NoType y devolver en su lugar True o False
    connectfind = Conexion("select moneda_to from movements where moneda_to == ?;", [moneda])
    resultado = connectfind.res.fetchall()
    if resultado == []:
        return False
    else:
       connectfind.con.close()
       return True 


def delete_all():#funcion que borra todos los datos de form sqlite y permite volver a crear una nueva inversion
    connectDelete = Conexion("DELETE FROM movements;")
    connectDelete.con.commit()
    connectDelete.con.close()
    connectre = Conexion("SELECT * from movements")
    connectre.con.commit()
    connectre.con.close()
    return select_all
    

def valor_compra(moneda):#funcion que devuelve un float que seria el valor_compra
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

def cantidad_realcryp(moneda):#funcion que devuelve un float que seria el valor real que tenemos de crypto y que podemos utilizar por tradeo o venta
    if consulta_mon_from(moneda) == False:
        invertido = 0
    else:
        invertido = status_invertido(moneda)[0][0]
    if consulta_mon_to(moneda) == False:
        recuperado= 0
    else:
        recuperado=status_recuperado(moneda)[0][0]
    valor_compra=recuperado-invertido
    return valor_compra


def status_invertido(moneda):#suma todas las cantidades de una moneda en su cantidad_from,devuelve un valor en tupla
    connectInvertido = Conexion("select sum(cantidad_from) from movements where moneda_from == ?;", [moneda])
    resultado =  connectInvertido.res.fetchall()
    connectInvertido.con.close()
    return resultado

def status_recuperado(moneda):#suma todas las cantidades de una moneda en su cantidad_to,devuelve un valor en tupla
    connectRecuperado = Conexion("select sum(cantidad_to) from movements where moneda_to == ?;", [moneda])
    resultado = connectRecuperado.res.fetchall()
    connectRecuperado.con.close()
    return resultado





def consulta_mon_from_to(moneda):#funcion que devuelve true o false segun si exsiste la moneda en base de datos
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

registros = select_all()
lista_criptos=["ETH","BNB","ADA","DOT","BTC","USDT","XRP","SOL","MATIC"]
lista_crypto_verificada=[]
for item in lista_criptos:
    if consulta_mon_from_to(item) == True:
         lista_crypto_verificada.append(item)
  

def valor_act():#funcion que calcula el valor actual de nuestra inversion, varios pasos
    lista_crypto_verificada= []#devuelve una lista con monedas que tenemos en realidad,para no obtener NoType
    for item in lista_criptos:
        if consulta_mon_from_to(item) == True:
            lista_crypto_verificada.append(item)

    lista_crypto_from=[]#devuelve una lista con monedas que tenemos en moneda_from,para no obtener NoType
    for item in lista_crypto_verificada:
        if consulta_mon_from(item)== True:
            lista_crypto_from.append(item)

    lista_crypto_to=[]#devuelve una lista con monedas que tenemos en moneda_to ,para no obtener NoType
    for item in lista_crypto_verificada:
        if consulta_mon_to(item)== True:
            lista_crypto_to.append(item)
    
    lista_valor_actual_cada_crypto = [] #devuelve una lista con todos los valores actual de cada cripto
    for crypto in lista_crypto_verificada:
        cambio_in_euros= change_crypto(crypto)#por cada cripto en cantidad_to calcula su suma y entonces el estados_recuperado
        if crypto in lista_crypto_to:
            recuperado=status_recuperado(crypto)[0][0]
        else: recuperado=0#evito de recibir no type

        if crypto in lista_crypto_from:#por cada cripto en cantidad_from calcula su suma y entonces el estados_invertido
                invertido=status_invertido(item)[0][0]
        else: invertido = 0#evito recibir notype
        
    
    
        cantidad_real_crypto = recuperado - invertido#cantidad que tenemos realmente de cada crypto
        valoractualcrypto= (cambio_in_euros * cantidad_real_crypto)#moltiplico el valor en euros por la cantidad de crypto que tengo
        lista_valor_actual_cada_crypto.append(valoractualcrypto)#adjunto a una lista todos los valores actuales de todas las crypto
        resultado= sum(lista_valor_actual_cada_crypto)#sumo tosos los valores
        return resultado#devuelve un float
