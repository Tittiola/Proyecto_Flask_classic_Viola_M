from registro_ig import app
from datetime import date,datetime
from flask import render_template,request,redirect,url_for
from registro_ig.models import select_all,insert,change_from_to,status_invertido

@app.route("/")
def index():

    registros = select_all()

    datos_mov=[
        {"id":1, "date":"2023-25-01", "time":"11:55", "moneda_from":"EUR", "cantidad_from":1000.0, "moneda_to":"BTC", "cantidad_to":"0.2"}
    ]
    return render_template("index.html",pageTitle="Todos",data=registros)#data esta en index con jinja, y aqui creamos la variable asignandole la lista de diccionario data_mov




@app.route("/purchase",methods=["GET","POST"])
def purchase():
    
    #breakpoint()
    if request.method == "GET":
        return render_template("purchase.html",form={})
    else:#entra nel post y son 2 post
        if 'calcular' in request.form:#primer boton y primer post
        
            cantidad_from=float(request.form['cantidad_from'])
            moneda_from=request.form['moneda_from']
            moneda_to=request.form['moneda_to']
            cambio=change_from_to(moneda_from,moneda_to)
            precio_unitario = cantidad_from/cambio
            
            lista_request={
                "moneda_from":request.form['moneda_from'],
                "moneda_to":request.form['moneda_to'],
                "cantidad_from":request.form['cantidad_from'],
                "cantidad_to":str(cambio),
                "precio_unitario":str(precio_unitario)
            }


            return render_template("purchase.html", form=lista_request, precio_unitario=precio_unitario)
        
        if 'comprar' in request.form:
            registros = select_all()
            
            
            insert([ "2023-01-01",
                     "11:01",
                     request.form['moneda_from'],
                     request.form['cantidad_from'],
                     request.form['moneda_to'],
                     request.form['cantidad_to'] ])

            return redirect("/")
        


    


@app.route("/status", methods=["GET","POST"] )
def resume():
    if request.method == "GET":
        invertido=status_invertido("EUR")[0][0]
    
        breakpoint()
    
    
        return render_template("status.html", invertido=invertido)
        
    else:
        pass
    




