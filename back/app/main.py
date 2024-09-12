from fastapi import FastAPI, Request, HTTPException
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
import IP2Location
import os
from fastapi import FastAPI, Header, HTTPException, status


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)


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





def check_invalid_ip(rec):
    """Verifica si hay un valor de IP inválido en el diccionario."""
    for key, value in rec.items():
        if "INVALID IP ADDRESS" in value:
            raise HTTPException(status_code=400, detail="Invalid IP address value in the record")
        elif "-" in value:
            raise HTTPException(status_code=404, detail="Resource not found")



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



