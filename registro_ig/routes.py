from registro_ig import app
from datetime import date,datetime
from flask import render_template,request,redirect
from registro_ig.models import *
from registro_ig.valor_Actual import valor_act


"""def validatePurchse(requestForm, moneda_from, valor_compra):
    errores=[]
    if requestForm['cantidad_from'] <= 0:
        errores.append("cantidad invalida: Inserte una cantidad mayor de 0")
    if requestForm['moneda_from'] ==  requestForm['moneda_from']:
        errores.append("moneda invalida: No puede intercambiar valores con la misma mondeda")
    if requestForm['moneda_from'] != "EUR" and requestForm['cantidad_from']> valor_compra(moneda_from):
       
    return errores"""

@app.route("/")
def index():

    registros = select_all()

    datos_mov=[
        {"id":1, "date":"2023-25-01", "time":"11:55", "moneda_from":"EUR", "cantidad_from":1000.0, "moneda_to":"BTC", "cantidad_to":"0.2"}
    ]
    return render_template("index.html", page ="Home", pageTitle="Todos",data=registros)#data esta en index con jinja, y aqui creamos la variable asignandole la lista de diccionario data_mov




@app.route("/purchase",methods=["GET","POST"])
def purchase():
    
    #breakpoint()
    if request.method == "GET":
        return render_template("purchase.html",page ="purchase",form={})
    else:#entra nel post y son 2 post
        cantidad_from=float(request.form['cantidad_from'])
        moneda_from=request.form['moneda_from']
        moneda_to=request.form['moneda_to']
            
        valo = status_recuperado(moneda_from)
        

        if 'calcular' in request.form:#primer boton y primer post
            errores=[]
            if moneda_from != "EUR":
                if float(cantidad_from) > valo[0][0] or float(cantidad_from) == "NoneType":
                    errores.append("Cantidad insuficiente, o moneda inexsistente en su cartera")
                if moneda_from == moneda_from:
                    errores.append("No se pueden intercambiar la mismas monedas")
                if moneda_from != "EUR" and consulta_mon_from(moneda_from) == False:
                    errores.append("No tiene este tipo de criptomoneda")
                if moneda_from == "NoneType":
                    errores.append("No tiene este tipo de criptomoneda")
            elif moneda_to == "EUR"and moneda_from != "BTC":
                    errores.append("No puede vender una moneda diferente de BTC a Euros"
            else:
                cambio=change_from_to(moneda_from,moneda_to)
        
            
          
            
            
            


            precio_unitario = cantidad_from/cambio
            
            lista_request={
                "moneda_from":request.form['moneda_from'],
                "moneda_to":request.form['moneda_to'],
                "cantidad_from":request.form['cantidad_from'],
                "cantidad_to":str(cambio),
                "precio_unitario":str(precio_unitario)
            }


            return render_template("purchase.html", form=lista_request, msgError=errores, precio_unitario=precio_unitario)
        
        if 'comprar' in request.form:
            registros = select_all()
            fecha = datetime.now().strftime('%Y-%m-%d')
            horas = datetime.now().strftime('%H:%M:%S')
            
            
        
            insert([ fecha,
                     horas,
                     request.form['moneda_from'],
                     request.form['cantidad_from'],
                     request.form['moneda_to'],
                     request.form['cantidad_to'] ])

            return redirect("/")
      


    


@app.route("/status", methods=["GET","POST"] )
def resume():
    if request.method == "GET":
        invertido=status_invertido("EUR")[0][0]
        recuperado=status_recuperado("EUR")[0][0]
        valor_compr= valor_compra("EUR")
        valor_actual=valor_act()
        
        
        return render_template("status.html", page ="status", valor_actual=valor_actual, invertido=invertido, recuperado=recuperado,valor_compra=valor_compr, form={})
    else:
        if 'reiniciar' in request.form:
            delete_all()
            return redirect("/") 
        
        
        
