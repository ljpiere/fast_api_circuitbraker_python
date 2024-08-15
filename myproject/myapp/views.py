# myapp/views.py

from django.shortcuts import render
from circuitbreaker import CircuitBreaker, CircuitBreakerError
import requests
import logging
import time

logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

class MyCircuitBreaker(CircuitBreaker):
    FAILURE_THRESHOLD = 2
    RECOVERY_TIMEOUT = 10
    EXPECTED_EXCEPTION = (requests.ConnectionError, requests.RequestException, requests.Timeout)

@MyCircuitBreaker()
def call_external_api():
    BASE_URL = "https://6iqdf9i7w9.execute-api.us-east-1.amazonaws.com/dev"
    END_POINT = "dev"
    resp = requests.get(f"{BASE_URL}/{END_POINT}")
    resp.raise_for_status()  # Esto lanzará una excepción si hay un error HTTP
    return resp.json()


def index(request):
    try:
        data = call_external_api()
        return render(request, "index.html", {"data": data})
    except CircuitBreakerError:
        message = "La solicitud ha fallado repetidamente. El Circuit Breaker se ha activado para evitar más intentos por un tiempo."
        return render(request, "error.html", {"message": message, "circuit_breaker": True}, status=503)
    except Exception as e:
        message = f"Ocurrió un error al intentar conectarse a la API: {str(e)}"
        return render(request, "error.html", {"message": message, "circuit_breaker": False}, status=503)

