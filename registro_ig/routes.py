from registro_ig import app
from datetime import date,datetime
from flask import render_template,request,redirect
from registro_ig.models import select_all,status_recuperado,status_invertido,change_from_to,insert,valor_compra,delete_all,valor_act,cantidad_realcryp

#funcion que controla los errores
def validatePurchase(requestForm):
    lista_criptos=["ETH","BNB","ADA","DOT","BTC","USDT","XRP","SOL","MATIC"]
    moneda_to=requestForm['moneda_to']
    moneda_from=requestForm['moneda_from']
    cantidad_from=requestForm['cantidad_from']
    errores=[]
    if moneda_from != "EUR" and moneda_from  != lista_criptos:
        errores.append("Moneda inexsistente en su cartera")
    if moneda_from ==  moneda_to:
        errores.append("Moneda invalida: No puede intercambiar valores con la misma mondeda")
    if moneda_from != "EUR" and float(cantidad_from) > cantidad_realcryp(moneda_from):
        errores.append("Cantidad insuficiente, o moneda inexsistente en su cartera")
    if float(cantidad_from) <= 0:
        errores.append("No puede introducir cantidad inferior a 1")
       
    return errores


@app.route("/")#Home
def index():

    registros = select_all()#importo todo el registro

    return render_template("index.html", page ="Home", pageTitle="Home",data=registros)#data esta en index con jinja, y aqui creamos la variable asignandole la lista de diccionario data_mov


@app.route("/purchase",methods=["GET","POST"])
def purchase():
    
    if request.method == "GET":
        return render_template("purchase.html",page ="purchase",form={})
    else:#entra nel post y son 2 POST
        cantidad_from=float(request.form['cantidad_from'])
        moneda_from=request.form['moneda_from']
        moneda_to=request.form['moneda_to']
        
        if 'calcular' in request.form:#primer boton y primer post

            errores = validatePurchase(request.form)
            if errores:#si hay errores no calcula
                return render_template("purchase.html",msgError=errores, form={})
        
            else:
                cambio=change_from_to(moneda_from,moneda_to)#peticion api del intercambio
                precio_unitario = cantidad_from/cambio
                
                lista_request={
                    "moneda_from":request.form['moneda_from'],
                    "moneda_to":request.form['moneda_to'],
                    "cantidad_from":request.form['cantidad_from'],
                    "cantidad_to":str(cambio),
                    "precio_unitario":str(precio_unitario)
                }#declaro la lista de los argumentos del form para que se devuelvan en los botones 
                
                return render_template("purchase.html", form=lista_request, pageTitle="Invertir", msgError=errores, precio_unitario=precio_unitario)
        
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
        invertido=status_invertido("EUR")[0][0]
        recuperado=status_recuperado("EUR")[0][0]
        valor_compr= valor_compra("EUR")
        valor_actual=valor_act()#funcion que captura el valor actual de euros con las cryptomonedas que efectivamente se poseen
        
        return render_template("status.html", pageTitle="Status", valor_actual=valor_actual, invertido=invertido, recuperado=recuperado,valor_compra=valor_compr, form={})
        
    else:
        if 'reiniciar' in request.form:
            delete_all()
            return redirect("/")