Hola,

TomatuIP Perro, consiste en obtener la ip publica sea ipv4 o ipv6 y su informacion geografica, esta es ultima se obtiene mediante una base de datos de `IP2location`

`https://lite.ip2location.com`


El proyecto esta estructurado de la siguiente forma

`BACK`: Esta constituido por varios endpoint, uno de estos es `/get-ip` que recibe como parametro una ip
el cual esta hace una consulta a las diferentes bases de datos `./app/DB1_IP6.BIN` este contiene las IPV6 y
las IPV4 las contiene `'./app/IP2LOCATION-LITE-DB3.BIN'`
El otro endpoint `/auth` hasta ahora, se encarga de validar las solicitudes hacia el servicio de `jeankis`.

Deesarrollado: `FastAPI`
Despliegue: `uvicorn`

`FRONT`:En este se encuentra toda la interfaz grafica.

Desarrollado: `angular`
Despliegue: `node.js`

`BACK/nginx`: Aqui se encuentras las configuraciones necesarias para la ejecucion de nginx, que hara de balanceador a todas las solicitudes.

`BACK/ngrok.yml`: Aqui se encuentra parte de las configuraciones de ngrok que hara de tunel de nginx hacia un dominio publico

`Carpeta raiz`: 

Todas estas instancias se crean en docker con docker compose, en la carpeta raiz del proyecto se encuentra el `docker-compose.yml` el cual orquesta todos los contenedores

`jeankinsfile` este archivo contiene la configuracion para el pipeline que valida el push al repositorio, se ayuda del archivo `BACK/test.py` para validar que los cambios al backend sean correctos y que no se caiga produccion xd, pero eso esta en proceso.

