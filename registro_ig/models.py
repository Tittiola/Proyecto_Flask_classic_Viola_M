import sqlite3
import requests
#from registro_ig import routes
from config import apiKey, ORIGIN_DATA




def change_from_to(moneda1, moneda2):
    consulta = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{moneda1}/{moneda2}?apikey={apiKey}')
    #breakpoint()
    Q = consulta.json()
    return Q["rate"]




def select_all():#importo todo lo que hay en el form sql a la pagina html
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()

    res= cur.execute("select id,date,time,moneda_from,cantidad_from,moneda_to,cantidad_to from movements order by date;")
   
    filas = res.fetchall()#capturo las filas de datos
    columnas= res.description#capturo los nombres de columnas

    #objetivo crear una lista de diccionario con filas y columnas

    resultado =[]#lista para guadar diccionario
   
    for fila in filas:
        dato={}#crear un diccionario para cada registro
        posicion=0#crear una posicion de columna para adjuntar y incrementar

        for campo in columnas:
            dato[campo[0]]=fila[posicion]#el campo columna es siempre en 0
            posicion += 1
        resultado.append(dato)


    return resultado






def insert(registro):
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()

    cur.execute("insert into movements(date,time,moneda_from,cantidad_from,moneda_to,cantidad_to) values(?,?,?,?,?,?)",registro)

    con.commit()#funcion que registra finalmente

    con.close()



"""class Exchange:
    def __init__(self,criptofrom, criptoto):
        self.cripto_first_change = criptofrom
        self.cripto_second_change = criptoto
        self.rate = None
        self.time = None
        self.r = None
        self.resultado = None

'''def insert()
   

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
