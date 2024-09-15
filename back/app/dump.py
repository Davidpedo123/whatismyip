import redis
import IP2Location
import json
from concurrent.futures import ThreadPoolExecutor

# Inicializar la base de datos IP2Location
database = IP2Location.IP2Location('IP2LOCATION-LITE-DB3.BIN')

# Solucionar el problema de la excepción en el iterador
database.original_ip = ''

# Función generadora para obtener datos
def generate_data():
    try:
        for record in database:
            yield record.__dict__  # Convertir objeto a diccionario y usar yield
    except Exception as e:
        print(f"Error al iterar sobre la base de datos: {e}")

# Función para almacenar un único item en Redis
def store_in_redis(item):
    ip = item.get('ip')
    if ip:
        json_data = json.dumps(item)  # Convertir el diccionario a JSON
        redis_client.set(ip, json_data)  # Almacenar la cadena JSON en Redis

# Configurar el cliente de Redis
redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    password="a97f7a7c3c7101d9d15c55e6fba8a2bf393bf05489ace790f8606414668d538c"
)

# Usar ThreadPoolExecutor para almacenar datos en paralelo
with ThreadPoolExecutor(max_workers=10) as executor:
    for item in generate_data():
        executor.submit(store_in_redis, item)

print("Datos almacenados en Redis con éxito.")
