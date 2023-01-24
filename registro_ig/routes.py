from registro_ig import app
from flask import render_template
import requests

class ModelError(Exception):
    pass


class Exchange:
    def __init__(self,criptofrom, criptoto):
        self.cripto_first_change = criptofrom
        self.cripto_second_change = criptoto
        self.rate = None
        self.time = None
        self.r = None
        self.resultado = None

    def updateExchange(self,apiKey):
        self.r = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{self.criptofrom}/{self.criptoto}?apikey={apiKey}')
        self.resultado = self.r.json()
        if self.r.status_code == 200:
            self.rate = self.resultado['rate']#si va bien
            self.time = self.resultado['time']
        else:    
            raise ModelError( f"status: {self.r.status_code} error: {self.resultado['error']} ")

        


@app.route("/")
def index():
    return render_template("index.html",pageTitle="Todos")

@app.route("/purchase")
def compra():
    conversion = Exchange
    return render_template("purchase.html",pageTitle="Todos", moneda_from=conversion(criptoto=))

@app.route("/status")
def estado():
    return render_template("status.html",pageTitle="Todos")