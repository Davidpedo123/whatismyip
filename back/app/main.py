import time  # Importamos el módulo time para medir el tiempo
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
import IP2Location
import os
import redis
import json
from app.configDB import redis_client
from fastapi import Header, HTTPException, status

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
GITHUB_TOKEN = token

def verify_github_token(token: str):
    if token != GITHUB_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/auth")
async def github_webhook(x_github_token: str = Header(None)):
    verify_github_token(x_github_token)
    return {"message": "Solicitud válida de GitHub"}

def check_invalid_ip(data):
    for key, value in data.items():
        if "INVALID IP ADDRESS" in value:
            raise HTTPException(status_code=400, detail="Invalid IP address value in the record")
        elif "-" in value:
            raise HTTPException(status_code=404, detail="Resource not found")

@app.get("/get-ip")
async def get_ip(request: Request, ip: str):
    try:
        # Medir el tiempo de consulta a Redis
        redis_start_time = time.time()
        
        data = redis_client.get(ip)
        
        redis_end_time = time.time()
        redis_duration = redis_end_time - redis_start_time
        print(f"Tiempo de respuesta de Redis: {redis_duration:.6f} segundos")
        
        if data is not None:
            data = json.loads(data.decode("UTF-8"))
        else:
            # Si no se encuentra en Redis, medir el tiempo de consulta a la base de datos
            db_start_time = time.time()
            
            if len(ip) > 15:
                # Base de datos para IPs IPv6
                database = IP2Location.IP2Location('./app/DB1_IP6.BIN')
                data = database.get_all(ip).__dict__
                print("Base de datos IP6")
            else:
                # Base de datos para IPs IPv4
                database = IP2Location.IP2Location('./app/IP2LOCATION-LITE-DB3.BIN')
                data = database.get_all(ip).__dict__
                print("Base de datos IP4")
            
            # Fin de la consulta a la base de datos
            db_end_time = time.time()
            db_duration = db_end_time - db_start_time
            print(f"Tiempo de respuesta de la base de datos: {db_duration:.6f} segundos")
            
            # Almacenar en Redis para futuras consultas
            redis_client.set(ip, json.dumps(data))

        check_invalid_ip(data)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return {"ip": data}
