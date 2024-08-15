# myapp/views.py
#-----------------------------------------------------------------------------------
# Basic DJango APP with a Python Circuit breaker
#
# Line 12: Check the time 
# Line 16: Circuit Breaker configuration:
#       FAILURE_THRESHOLD: Max retries
#       RECOVERY_TIMEOUT: Time to try again
#       EXPECTED_EXCEPTION: Which exception activate circuit breaker
# Line 26: Call the external API
# Line 35: Define index behaviour
#-----------------------------------------------------------------------------------

from django.shortcuts import render
from circuitbreaker import CircuitBreaker, CircuitBreakerError
import requests
import logging
# import time

logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

class MyCircuitBreaker(CircuitBreaker):
    FAILURE_THRESHOLD = 2 # Max retries
    RECOVERY_TIMEOUT = 10 # Time to try again
    EXPECTED_EXCEPTION = (requests.ConnectionError, requests.RequestException, requests.Timeout)

@MyCircuitBreaker()
def call_external_api():
    """Call to the external API

    Returns:
        json: Response or exception
    """
    BASE_URL = "https://6iqdf9i7w9.execute-api.us-east-1.amazonaws.com/dev"
    END_POINT = "dev"
    resp = requests.get(f"{BASE_URL}/{END_POINT}")
    resp.raise_for_status()  # Launch an Exception for HTTP error
    return resp.json()


def index(request):
    """Choose index.html or error.html

    Args:
        request (json): API request

    Returns:
        json: Message with an error (for an error or circuit breaker activate) or API responde it was OK.
    """
    try:
        data = call_external_api()
        return render(request, "index.html", {"data": data}) # Call the index if the API response is OK
    except CircuitBreakerError:
        message = "La solicitud ha fallado repetidamente. El Circuit Breaker se ha activado para evitar más intentos por un tiempo."
        return render(request, "error.html", {"message": message, "circuit_breaker": True}, status=503) # For 2 retries
    except Exception as e:
        message = f"Ocurrió un error al intentar conectarse a la API: {str(e)}"
        return render(request, "error.html", {"message": message, "circuit_breaker": False}, status=503) # First error (max two)