from registro_ig import app
from datetime import datetime
from flask import render_template,request,redirect
from registro_ig.models import *


#funcion que controla los errores
def validatePurchase(requestForm):
    moneda_to=requestForm['moneda_to']
    moneda_from=requestForm['moneda_from']
    cantidad_from=requestForm['cantidad_from']
    cantidad_realcry = (money_back(moneda_from)[0][0]) - (invested_money(moneda_from)[0][0])
    errores=[]
    if moneda_from != "EUR" and consult_currencies(moneda_from) == False:#evito resultado notype
        errores.append("Moneda inexsistente en su cartera")
    if moneda_from ==  moneda_to:
        errores.append("Moneda invalida: No puede intercambiar valores con la misma mondeda")
    if moneda_from != "EUR" and float(cantidad_from) > cantidad_realcry:#calculo si tengo en realidad la cantidad que pongo en cantidad_from
        errores.append("Cantidad insuficiente, o moneda inexsistente en su cartera")
    if float(cantidad_from) <= 0:
        errores.append("No puede introducir cantidad inferior a 1")
       
    return errores


@app.route("/")#Home
def index():

    registros = select_all()#importo todo el registro

    return render_template("index.html", page = "Inicio", pageTitle="Home",data=registros)#data esta en index con jinja, y aqui creamos la variable asignandole la lista de diccionario data_mov



@app.route("/purchase",methods=["GET","POST"])
def purchase():
   
    
    if request.method == "GET":
        
        return render_template("purchase.html",page ="Compra",form={})
    
    else:#entra nel post y son 2 POST
        cantidad_from=float(request.form['cantidad_from'])
        moneda_from=request.form['moneda_from']
        moneda_to=request.form['moneda_to']
        cantidad_to=request.form['cantidad_to']
        
        if 'calcular' in request.form:#primer boton y primer post

            errores = validatePurchase(request.form)
            if errores:#si hay errores no calcula
                return render_template("purchase.html",msgError=errores, page ="Compra",cantidad_from=cantidad_from, cantidad_to=cantidad_to, form={})
        
            else:
                
                cambio =change_from_to(moneda_from,moneda_to)#peticion api del intercambio
                
                precio_unitario = cantidad_from/cambio
                cantidad_to = cambio
                
                lista_request={
                    "moneda_from":request.form['moneda_from'],
                    "moneda_to":request.form['moneda_to'],
                    "cantidad_from":request.form['cantidad_from'],
                    "cantidad_to":str(cambio),
                    "precio_unitario":str(precio_unitario)
                }#declaro la lista de los argumentos del form para que se devuelvan en los botones 
                
                return render_template("purchase.html", page ="Compra", cantidad_to=cambio, form=lista_request, pageTitle="Invertir", msgError=errores, precio_unitario=precio_unitario)
        
        if 'comprar' in request.form:#segunda peticion "POST", finalmente capturo horas y fecha

            fecha = datetime.now().strftime('%Y-%m-%d')
            horas = datetime.now().strftime('%H:%M:%S')
            
            insert([ fecha,
                     horas,
                     request.form['moneda_from'],
                     request.form['cantidad_from'],
                     request.form['moneda_to'],
                     request.form['cantidad_to'] ])#funcion que captura y registra los datos en la base de datos

            return redirect("/")#devuelve a la home, donde se averiguerá la transacion efectuada
      


@app.route("/status", methods=["GET","POST"] )
def resume():
    if request.method == "GET":#calculos sobre la base de datos
        invertido=invested_money("EUR")[0][0]
        recuperado=money_back("EUR")[0][0]
        valor_compra= (invested_money("EUR")[0][0] - money_back("EUR")[0][0])
        valor_actual=current_value()#funcion que captura el valor actual de euros con las cryptomonedas que efectivamente se poseen
        
        return render_template("status.html", page ="Estado", valor_actual=valor_actual, invertido=invertido, recuperado=recuperado,valor_compra=valor_compra, form={})
        
    else:
        if 'reiniciar' in request.form:#he puesto un boton para poder poner a cero la tabla y volver a empezar la inversion
            delete_all()
            return redirect("/")