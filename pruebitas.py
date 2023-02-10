from registro_ig.models import *
import requests
from registro_ig.conexion import Conexion

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

print(consulta_mon_from_to("BTC"))

print(cantidad_realcryp("BTC"))
print(lista_crypto_verificada)