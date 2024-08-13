# myapp/views.py

from django.shortcuts import render
from circuitbreaker import CircuitBreaker, CircuitBreakerError
import requests
import logging

logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

class MyCircuitBreaker(CircuitBreaker):
    FAILURE_THRESHOLD = 1 # Vamos a mantener solo 1
    RECOVERY_TIMEOUT = 60
    EXPECTED_EXCEPTION = requests.exceptions.RequestException  # Captura todas las excepciones de requests
    #EXPECTED_EXCEPTION = (requests.RequestException, requests.ConnectionError, requests.Timeout)

@MyCircuitBreaker()
def call_external_api():
    BASE_URL = "https://6iqdf9i7w9.execute-api.us-east-1.amazonaws.com/dev"
    END_POINT = "dev"
    try:
        resp = requests.get(f"{BASE_URL}/{END_POINT}")
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, requests.ConnectionError, requests.Timeout) as e:
        logger.error(f"Error al conectar con la API: {e}")
        raise

def index(request):
    try:
        data = call_external_api()
        return render(request, "index.html", {"data": data})
    except CircuitBreakerError:
        # Mensaje claro cuando se activa el circuit breaker
        message = "La solicitud ha fallado repetidamente. El Circuit Breaker se ha activado para evitar más intentos por un tiempo."
        return render(request, "error.html", {"message": message, "circuit_breaker": True}, status=503)
    except Exception as e:
        # Otros errores que no son del circuit breaker
        message = f"Ocurrió un error al intentar conectarse a la API: {str(e)}"
        return render(request, "error.html", {"message": message, "circuit_breaker": False}, status=503)
