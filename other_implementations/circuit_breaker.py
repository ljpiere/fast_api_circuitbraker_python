from fastapi import FastAPI
import circuitbreaker
import requests
import logging

app = FastAPI()
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

class MyCircuitBreaker(circuitbreaker.CircuitBreaker):
    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 60
    EXPECTED_EXCEPTION = (requests.RequestException, requests.ConnectionError, requests.Timeout)

@MyCircuitBreaker()    
def call_external():
    BASE_URL = "https://swap1.dev"
    END_POINT = "api/planets/1/"
    try:
        resp = requests.get(f"{BASE_URL}/{END_POINT}")
        resp.raise_for_status()  # Esto generará una excepción si el código de estado no es 200-299
        data = resp.json()
    except (requests.RequestException, requests.ConnectionError, requests.Timeout) as e:
        logger.error(f"Error al conectar con la API: {e}")
        raise  # Esto permitirá que el circuit breaker capture la excepción
    return data

@app.get("/")
def implement_circuit_breaker():
    try:
        data = call_external()
        return {
            "status_code": 200,
            "success": True,
            "message": "Success get starwars data", 
            "data": data
        }
    except circuitbreaker.CircuitBreakerError as e:
        return {
            "status_code": 503,
            "success": False,
            "message": f"Circuit breaker active: {e}"
        }
    except requests.RequestException as e:
        return {
            "status_code": 503,
            "success": False,
            "message": f"Request failed: {e}"
        }
