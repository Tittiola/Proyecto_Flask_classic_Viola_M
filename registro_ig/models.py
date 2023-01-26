import sqlite3
from config import *
#from registro_ig.conexion import Conexion


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
    connectInsert = Conexion("insert into movements(date,concept,quantity) values(?,?,?)",registro)
    connectInsert.con.commit()#funcion que registra finalmente
    connectInsert.con.close()

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
    '''
