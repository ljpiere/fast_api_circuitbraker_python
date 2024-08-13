# Circuit braker using FastApi and Python in AWS

```jsx
from fastapi import FastAPI
import circuitbreaker
import requests
import logging

```

- **Imports:**
    - `FastAPI`: A modern, fast (high-performance) web framework for building APIs with Python 3.6+.
    - `circuitbreaker`: A library for implementing the Circuit Breaker design pattern.
    - `requests`: A popular HTTP library for making requests.
    - `logging`: Python's standard logging module for tracking events during program execution.

```jsx
app = FastAPI()
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

```

- **App Initialization and Logging Configuration:**
    - `app = FastAPI()`: Creates an instance of the FastAPI application.
    - `logging.basicConfig(...)`: Sets the basic configuration for logging, including the date format and logging level.
    - `logger = logging.getLogger()`: Retrieves a logger instance for logging messages.

```jsx
class MyCircuitBreaker(circuitbreaker.CircuitBreaker):
    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 60
    EXPECTED_EXCEPTION = (requests.RequestException, requests.ConnectionError, requests.Timeout)

```

- **Custom Circuit Breaker Class:**
    - `class MyCircuitBreaker(circuitbreaker.CircuitBreaker)`: Defines a custom circuit breaker class extending the `CircuitBreaker` class from the `circuitbreaker` library.
    - `FAILURE_THRESHOLD = 5`: The number of consecutive failures before the circuit breaker trips.
    - `RECOVERY_TIMEOUT = 60`: The time (in seconds) to wait before attempting to reset the circuit breaker.
    - `EXPECTED_EXCEPTION = (requests.RequestException, requests.ConnectionError, requests.Timeout)`: Exceptions that should be considered failures by the circuit breaker.

```jsx
@MyCircuitBreaker()
def call_external():
    BASE_URL = "<https://swap1.dev>"
    END_POINT = "api/planets/1/"
    try:
        resp = requests.get(f"{BASE_URL}/{END_POINT}")
        resp.raise_for_status()  # This will raise an exception if the status code is not 200-299
        data = resp.json()
    except (requests.RequestException, requests.ConnectionError, requests.Timeout) as e:
        logger.error(f"Error connecting to API: {e}")
        raise  # This will allow the circuit breaker to capture the exception
    return data

```

- **External Call Function with Circuit Breaker:**
    - `@MyCircuitBreaker()`: Decorates the function with the custom circuit breaker, applying its logic.
    - `BASE_URL = "<https://swap1.dev>"`: Sets the base URL for the external API.
    - `END_POINT = "api/planets/1/"`: Sets the specific endpoint for the API call.
    - `resp = requests.get(f"{BASE_URL}/{END_POINT}")`: Makes a GET request to the specified API endpoint.
    - `resp.raise_for_status()`: Raises an exception if the HTTP status code is not in the range 200-299.
    - `data = resp.json()`: Parses the response JSON into a Python dictionary.
    - `except (requests.RequestException, requests.ConnectionError, requests.Timeout) as e`: Catches specific exceptions that are considered failures.
    - `logger.error(f"Error connecting to API: {e}")`: Logs the error message.
    - `raise`: Re-raises the caught exception to be handled by the circuit breaker.

```jsx
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

```

- **API Route and Circuit Breaker Implementation:**
    - `@app.get("/")`: Defines a GET route at the root URL (`/`) for the FastAPI application.
    - `def implement_circuit_breaker()`: Function to handle requests to the root URL.
    - `data = call_external()`: Calls the `call_external` function to fetch data from the external API.
    - `return {...}`: Returns a JSON response containing the status code, success flag, message, and data.
    - `except circuitbreaker.CircuitBreakerError as e`: Catches exceptions raised by the circuit breaker.
    - `return {...}`: Returns a JSON response indicating that the circuit breaker is active.
    - `except requests.RequestException as e`: Catches request-related exceptions.
    - `return {...}`: Returns a JSON response indicating that the request failed.