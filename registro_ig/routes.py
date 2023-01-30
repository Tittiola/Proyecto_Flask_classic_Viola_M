from registro_ig import app
from flask import render_template,request,redirect,url_for
from registro_ig.models import select_all,insert,change_from_to


'''
class ModelError(Exception):
    pass




    def updateExchange(self,apiKey):
        self.r = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{self.criptofrom}/{self.criptoto}?apikey={apiKey}')
        self.resultado = self.r.json()
        if self.r.status_code == 200:
            self.rate = self.resultado['rate']#si va bien
            self.time = self.resultado['time']
        else:    
            raise ModelError( f"status: {self.r.status_code} error: {self.resultado['error']} ")
            '''

        
@app.route("/")
def index():

    registros = select_all()

    datos_mov=[
        {"id":1, "date":"2023-25-01", "time":"11:55", "moneda_from":"EUR", "cantidad_from":1000.0, "moneda_to":"BTC", "cantidad_to":"0.2"}
    ]
    return render_template("index.html",pageTitle="Todos",data=registros)#data esta en index con jinja, y aqui creamos la variable asignandole la lista de diccionario data_mov




@app.route("/purchase",methods=["GET","POST"])
def compra():
    if request.method == "GET":
        return render_template("purchase.html")
    else:
        moneda_from=moneda_from
        moneda_to=moneda_to
        cantidad_to=""
        cambio_unidad=change_from_to(moneda_from,moneda_to)
        
        return render_template("purchase.html",moneda_from=moneda_from,moneda_to=moneda_to,cambio_unidad=cantidad_to,dataForm=request.form)
        
        
        #change_from_to conversion y almacenarla en Q
        #multiplcacion cantidad_from con q y almacenarla en pu
        #insert([ request.form['moneda_from'], request.form['moneda_to'], request.form['cantidad_from']  ])
        cantidad_from=cantidad_from

            
    #return render_template("purchase.html",cantidad_from=cantidad_from)


"""@app.route("/purchase")
def compra():
    pass
    return render_template("purchase.html")"""
        
       
       
       
       
'''moneda_from=moneda_from moneda_to=moneda_to
         cantidad_to = cantidad_to
        return render_template("/purchase.html",pageTitle = "Todos", moneda_from=moneda_from,moneda_to=moneda_to,cantidad_to=cantidad_to )
        change = change_from_to(moneda_from,moneda_to)

    
    return render_template("/purchase.html",pageTitle = "Todos", cambio=change )'''



    


        




@app.route("/status")
def resume():
    return render_template("status.html")




        
        
        
"""else:
        return render_template("purchase.html",pageTitle="Todos",data={})
        request.form #recibo dal formulario una tupla con los datos
           
           
           
("purchase.html",pageTitle="Todos", moneda_from=conversion(criptoto=))


@app.route("/status")
def estado():
    return render_template("status.html",pageTitle="Todos")"""
   