import requests

def test_search_ip(url, ip_address):
    # Construir la URL correctamente
    try:
        response = requests.get(f"{url}/get-ip?ip={ip_address}")
        status_code = response.status_code
        
        if status_code == 500:
            return "Validación Fallida: Error Interno del Servidor"
        elif status_code == 404:
            return "Validación Fallida: Problemas en la Base de Datos"
        else:
            return f"VALIDACION EXITOSA: {status_code}"
    except:
        return "Error: No se pudo establecer la comunicacion"

# Ejemplo de uso
print(test_search_ip("http://web-back:8050", "8.8.8.8"))
