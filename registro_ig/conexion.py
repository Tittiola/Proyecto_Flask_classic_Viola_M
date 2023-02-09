import sqlite3#conexion con libreria sqlite
from config import *
ORIGIN_DATA="data/movimientos.sqlite"


class Conexion:
    def __init__(self,querySql,params=[]):
        self.con = sqlite3.connect(ORIGIN_DATA)#conexion con la variable creada con mi base de datos en data/
        self.cur = self.con.cursor()#crear objecto de conexion
        self.res = self.cur.execute(querySql,params)#para recuperar datos de base de datos.
        #querySql seria "SELECT id,date,...FROM movements order by date'''
