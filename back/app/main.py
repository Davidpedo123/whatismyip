from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import IP2Location
import os
from fastapi import FastAPI, Header, HTTPException, status


app = FastAPI()

token = os.environ['TOKEN_GITHUB']
# Define un token estático que GitHub debe enviar
GITHUB_TOKEN = token

# Verifica si el token en las solicitudes es válido
def verify_github_token(token: str):
    if token != GITHUB_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/auth")
async def github_webhook(x_github_token: str = Header(None)):
    # Verifica el token
    verify_github_token(x_github_token)
    
    # Aquí procesarías el evento de GitHub
    return {"message": "Solicitud válida de GitHub"}





# Configura la carpeta donde estarán tus templates de Jinja2
templates = Jinja2Templates(directory="app/template")
app.mount("/asset", StaticFiles(directory="app/asset"), name="asset")

def check_invalid_ip(rec):
    """Verifica si hay un valor de IP inválido en el diccionario."""
    for key, value in rec.items():
        if "INVALID IP ADDRESS" in value:
            raise HTTPException(status_code=400, detail="Invalid IP address value in the record")
        elif "-" in value:
            raise HTTPException(status_code=404, detail="Resource not found")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    client_ip = request.client.host  # Captura la IP del cliente

    # Verifica si hay un encabezado 'X-Forwarded-For' para capturar la IP real detrás de un proxy
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        client_ip = forwarded_for.split(',')[0].strip()  # La primera IP es la real en caso de múltiples proxies
    
    print(client_ip)
    
    try:
        if len(client_ip) > 15:
            # Base de datos para IPs IPv6
            database = IP2Location.IP2Location('./app/DB1_IP6.BIN')
            rec = database.get_all(client_ip).__dict__
            
            # Verificar valores inválidos
            check_invalid_ip(rec)
            
            print("Base de datos IP6")
        else:
            # Base de datos para IPs IPv4
            database = IP2Location.IP2Location('./app/IP2LOCATION-LITE-DB3.BIN')
            rec = database.get_all(client_ip).__dict__
            
            print("Base de datos IP4")
        
    except HTTPException as e:
        # Manejar excepciones específicas
        raise e
    except Exception as e:
        # Manejar otros errores generales
        print(f"Error: {e}")  # Opcional, para depuración
        raise HTTPException(status_code=404, detail="Resource not found")

    return templates.TemplateResponse("index.html", {"request": request, "client_ip": client_ip, "rec": rec})

@app.get("/get-ip")
async def get_ip(request: Request, ip: str):
    try:
        if len(ip) > 15:
            # Base de datos para IPs IPv6
            database = IP2Location.IP2Location('./app/DB1_IP6.BIN')
            rec = database.get_all(ip).__dict__
            
            # Verificar valores inválidos
            check_invalid_ip(rec)
            
            print("Base de datos IP6")
        else:
            # Base de datos para IPs IPv4
            database = IP2Location.IP2Location('./app/IP2LOCATION-LITE-DB3.BIN')
            rec = database.get_all(ip).__dict__
            
            # Verificar valores inválidos
            check_invalid_ip(rec)
            
            print("Base de datos IP4")
    
    except HTTPException as e:
        # Manejar excepciones específicas
        raise e
    except Exception as e:
        # Manejar otros errores generales
        print(f"Error: {e}")  # Opcional, para depuración
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return {"ip": rec}



