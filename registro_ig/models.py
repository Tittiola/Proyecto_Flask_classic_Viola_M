import sqlite3
import requests
#from registro_ig import routes
#from config import apiKey
from registro_ig.conexion import Conexion
ORIGIN_DATA="data/movimientos.sqlite"
apiKey='24E07BC2-CA11-4FD2-9F14-889CEE3B8DBF'





def change_from_to(moneda1, moneda2):
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{moneda1}/{moneda2}?apikey={apiKey}')
    #breakpoint()
    Q = consulta.json()
    return Q["rate"]


def change_crypto(moneda):
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{moneda}/EUR?apikey={apiKey}')
    #breakpoint()
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

"""def valor_actual(moneda):  
    suma_to = Conexion("select sum(cantidad_to) from movements where moneda_to == ?;", [moneda])
    suma_from = Conexion("select sum(cantidad_from) from movements where moneda_from == ?;", [moneda])
    resultado_to = suma_to.res.fetchall()
    resultado_from = suma_from.res.fetchall()
    total_actual_moneda=resultado_to-resultado_from
    valor_unidad_cripto=change_from_to(moneda,"EUR")#averiguo el valor en euro actual de la cripto
    valor_actual_cripto=valor_unidad_cripto*total_actual_moneda#calculo el valor actual de la cripto en la cartera

    suma_to.con.close()
    suma_from.con.close()

    return valor_actual_cripto#devuelve el valor actual de una cripto, hay que sumarlo al valor de todas cripto exsistientes"""




    
   


    




"""def compra(moneda_from, moneda_to):
    if moneda_from == "EUR":
        pass
    else:
        return "error"

def tradeo(moneda_from, moneda_to):
    if moneda_from != "EUR" and moneda_from >= ORIGIN_DATA.(sum todas) 








   

def select_by(id):
    connectSelectBy=Conexion(f"select id,date,concept,quantity from movements where id={id}")
    resultado = connectSelectBy.res.fetchall()#res.fetchall captura las filas de datos
    connectSelectBy.con.close()
    return resultado[0]

def delete_by(id):
    connectDeleteBy=Conexion(f"delete from movements where id={id}")
    connectDeleteBy.con.commit()
    connectDeleteBy.con.close()

def update_by(id,registro):#['date','concept','quantity']
    connectUpdate=Conexion(f"UPDATE movements SET date=?,concept=?,quantity=? WHERE id={id}",registro)
    connectUpdate.con.commit()
    connectUpdate.con.close()


def select_by(id):
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()

    res = cur.execute(f"select id,date,concept,quantity from movements where id={id}")

    resultado = res.fetchall()

    con.close()

    return resultado[0]
    """
