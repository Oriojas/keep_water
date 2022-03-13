# keep_water
Fork the system

## Versión python
3.8.12

## Librerias a utilizar
* pandas: tratamiento de datos
* pyodbc: conexión base de datos mysql
* web3: conexiones blockchain
* plotly: visualizaciones
* FastAPI: creación de end points

## Infraestructura
La aplicación esta desplegada en una instancia EC2 de aws de un nucleo y 500M de memoria ram con sistema operativo Ubuntu, utilizando la capa gratuita de aws, la base de datos esta alojada en una instancia RDS de mysql de AWS

## Dashboard
Se puede ingresar a la url <http://ec2-18-209-67-144.compute-1.amazonaws.com:8080/dashboard/> para ver en tiempo real las lcturas de los dos sensores intalados

## Hardaware
Sensor de humedad y temperatura DHT11 ESP8266 para este caso la versión V3 Protoboard y cables Instalar IDE de Arduino y las librerías del ESP8266

## Ejecutar en segundo plano el script
Estas líneas de código funcionan para linux, para otro sistema operativo se debe consultar la documentación correspondiente, se debe estar en la carpeta raíz del repositorio: `chmod +x api.py` y luego `nohup python3 api.py &`

Es importante que el archivo new_plot.py tenga permiso de lectura sin estar en root esto se hace con: `sudo chmod 777 new_plot.py`

