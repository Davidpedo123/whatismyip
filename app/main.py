from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import IP2Location
import os


app = FastAPI()

# Configura la carpeta donde estarán tus templates de Jinja2
templates = Jinja2Templates(directory="app/template")
app.mount("/asset", StaticFiles(directory="app/asset"), name="asset")

@app.get("/", response_class=HTMLResponse)
async def get_client_ip(request: Request):
    client_ip = request.client.host  # Captura la IP del cliente

    # Verifica si hay un encabezado 'X-Forwarded-For' para capturar la IP real detrás de un proxy
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        client_ip = forwarded_for.split(',')[0].strip()  # La primera IP es la real en caso de múltiples proxies
    
    # Renderiza el template HTML pasando la IP como contexto
    print(client_ip)
    """directory = "../DB/DB_IPV4/DB1"
    file_name = "IP2LOCATION-LITE-DB3.BIN"
    file_path = os.path.join(directory, file_name)
    """
    database = IP2Location.IP2Location('./app/IP2LOCATION-LITE-DB3.BIN')
    rec = database.get_all(client_ip)
    return templates.TemplateResponse("index.html", {"request": request, "client_ip": client_ip, "rec": rec})

