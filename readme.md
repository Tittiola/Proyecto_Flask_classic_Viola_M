# Aplicación Web Conversion-Inversion

- Programa hecho en python con el framework Flask, App Conversion Inversion, con motor de base de datos SQLite

## En su entorno de python ejecutar el comando

```
pip install -r requirements.txt
```
las libreria utilizada flask https://flask.palletsprojects.com/en/2.2.x/


## Crear el archivo oculto .env y agregar las siguientes lineas
```
FLASK_APP=main.py
FLASK_DEBUG=true
```

## Ejecucion con el .env
```
flask run
```
## Comando para ejecutar el servidor:
```
flask --app main run
```

## Comando para actualizar el servidor con cambios de codigo en tiempo real

```
flask --app main --debug run
```

## Comando especial para lanzar el servidor en un puerto diferente
Esto se utiliza en el caso que el puerto 5000 este ocupado

```
flask --app main run -p 5001
```

## Comando para lanzar en modo debug y con puerto cambiado
```
flask --app main --debug run -p 5001
```
## Acceder al listado general monedas
```
https://rest.coinapi.io/v1/exchanges/?apikey=24E07BC2-CA11-4FD2-9F14-889CEE3B8DBF
```
## Renombrar .env y config.py a env.template y config_template

. para mantener en git instrucciones no especificas

## URL con cambio (ex de ETH a EUR)

https://rest.coinapi.io/v1/exchangerate/ETH/EUR?apikey=24E07BC2-CA11-4FD2-9F14-889CEE3B8DBF

## Insatalacion pip install requests en init

. para peticiones http

## Import librerias requests, datetime

. para peticiones http y capturar horas y fecha

## En data info create sqlite, base de datos
```
. instrucciones para poder crear el mismo formulario