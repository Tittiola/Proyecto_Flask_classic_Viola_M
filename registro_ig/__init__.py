from flask import Flask
from config import apiKey

app = Flask(__name__,instance_relative_config=True)

import requests

#r = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{from}/{to}?apikey={apiKey}')

#r.status_code # devuelve el estado peticion web, 200 correcto
#r.text # devuelve el cambio en formato jsn con time, asset id base(MATIC) asset id quote(EUR) y rate que es el cambio
#resultado = r.json()  guardamos el r.jason en resultado(diccionario en python)


from registro_ig.routes import *