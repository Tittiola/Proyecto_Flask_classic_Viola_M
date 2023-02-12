import requests
from registro_ig.conexion import Conexion
from config import apiKey

#funciones con peticiones api

def change_from_to(coin1, coin2):#funcion que devuelve el cambio poniendo dos tipos de monedas
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{coin1}/{coin2}?apikey={apiKey}')
    Q = consulta.json()
    return Q["rate"]


def change_crypto(coin):#funcion que pide el cambio en Euros poniendo un tipo de crypto
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{coin}/EUR?apikey={apiKey}')
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


def delete_all():#funcion que borra todos los datos de form sqlite y permite volver a crear una nueva inversion
    connectDelete = Conexion("DELETE FROM movements;")
    connectDelete.con.commit()
    connectDelete.con.close()
    connectre = Conexion("SELECT * from movements")
    connectre.con.commit()
    connectre.con.close()
    return select_all
    

def invested_money(coin):#suma todas las cantidades de una moneda en su cantidad_from,devuelve un valor en tupla y evita el return NoType
    connectInvertido = Conexion("SELECT (case when (SUM(cantidad_from)) is null then 0 else SUM(cantidad_from) end) as tot FROM movements  WHERE moneda_from == ?;", [coin])
    resultado =  connectInvertido.res.fetchall()
    connectInvertido.con.close()
    return resultado


def money_back(coin):#suma todas las cantidades de una moneda en su cantidad_to,devuelve un valor en tupla y evita el return NoType
    connectInvertido = Conexion("SELECT (case when (SUM(cantidad_to)) is null then 0 else SUM(cantidad_to) end) as tot FROM movements  WHERE moneda_to == ?;", [coin])
    resultado =  connectInvertido.res.fetchall()
    connectInvertido.con.close()
    return resultado
    

def consult_currencies(coin):#funcion que devuelve true o false segun si exsiste la moneda en base de datos
    moneda_is_in_mon_from = Conexion("select moneda_from from movements where cantidad_from > 0 and moneda_from == ?;", [coin])
    resultado_from = moneda_is_in_mon_from.res.fetchall()
    moneda_is_in_mon_to = Conexion("select moneda_to from movements where cantidad_to  > 0 and moneda_to == ?;", [coin])
    resultado_to = moneda_is_in_mon_to.res.fetchall()
    if resultado_from == [] and resultado_to == []:
        return False
    else:
       moneda_is_in_mon_to.con.close()
       moneda_is_in_mon_from.con.close()
       return True 

  
def current_value():#funcion que calcula el valor actual de nuestra inversion en difernetes pasos
    list_criptos=["ETH","BNB","ADA","DOT","BTC","USDT","XRP","SOL","MATIC"]
    list_crypto_verificada= []#devuelve una lista con monedas que tenemos en realidad, para no obtener NoType
    for item in list_criptos:
        if consult_currencies(item) == True:
            list_crypto_verificada.append(item)
    
    list_valor_actual_cada_crypto = [] #devuelve una lista con todos los valores actual de cada cripto
    for crypto in list_crypto_verificada:
        cambio_in_euros= change_crypto(crypto)#por cada cripto en cantidad_to calcula su suma y entonces el estados_recuperado
        recuperado=money_back(crypto)[0][0]
        invertido=invested_money(crypto)[0][0]
        
        cantidad_real_crypto = recuperado - invertido#cantidad que tenemos realmente de cada crypto
        valoractualcrypto= (cambio_in_euros * cantidad_real_crypto)#moltiplico el valor en euros por la cantidad de crypto que tengo
        list_valor_actual_cada_crypto.append(valoractualcrypto)#adjunto a una lista todos los valores actuales de todas las crypto
        resultado= sum(list_valor_actual_cada_crypto)#sumo tosos los valores
        return resultado#devuelve un float