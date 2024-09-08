El funcionamiento de la aplicacion consiste, en 3 modulos, la app publicada con fastAPI, una base de datos de las GEOIP, perteneciente a IP2LOCATION, la orquestacion con docker

APP: Consiste en capturar la ip de la solicitud, mediante, request, exactamente `request.client.host`, en base a esa IP buscarla en la base de datos, hay varias, pero la que estoy usando se llama "IP2LOCATION-LITE-DB3.BIN", es una llena de IPV4 y por ultimo renderizar todas estas variables en el hmtl, mediante jinja 2.

DB: Hay varias bases de datos, tanto para ipv4 como para ipv6, la forma de crear la conexion es mediante: `IP2Location.IP2Location(PATH_FILE_DB)` y la consulta, mediante metodo .get_all(IP_CLIENT)
hay varias carpetas pero en general las DB se encuentran en la carpeta DB

Docker: El proyecto ejecuta docker compose para orquestar los contenedore, lo que son el de la web, que en este se encuentra el despliegue del servidor de uvicorn que despliegue la aplicacion de fastapi donde se encuentra la logica de la aplicacion, el otro contenedor es de nginx, que hace de balanceador de carga al servidor de uvicorn y por ultimo el de ngrok, que permite crear un tunel de nuestro proxi de nginx a un dominio.
