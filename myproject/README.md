# Circuit breaker en python

Implementaremos un "Circuit Breaker" en una aplicación Django para manejar las fallas en las solicitudes a una API externa (Lambda). A continuación se explica cada parte del código:

1. **Importaciones**:
    
    ```python
    from django.shortcuts import render
    from circuitbreaker import CircuitBreaker, CircuitBreakerError
    import requests
    import logging
    # import time
    
    ```
    
    Se importan las bibliotecas necesarias para el funcionamiento del código, incluyendo Django para el renderizado de plantillas, el módulo `circuitbreaker` para implementar el patrón Circuit Breaker, `requests` para hacer solicitudes HTTP, y `logging` para registrar eventos.
    
2. **Configuración del logger**:
    
    ```python
    logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
    logger = logging.getLogger()
    
    ```
    
    Configura el sistema de logging para registrar eventos con el formato y nivel de información especificados.
    
3. **Definición de la clase `MyCircuitBreaker`**:
    
    ```python
    class MyCircuitBreaker(CircuitBreaker):
        FAILURE_THRESHOLD = 2
        RECOVERY_TIMEOUT = 10
        EXPECTED_EXCEPTION = (requests.ConnectionError, requests.RequestException, requests.Timeout)
    
    ```
    
    Se define una clase `MyCircuitBreaker` que hereda de `CircuitBreaker`. Esta clase tiene tres configuraciones importantes:
    
    - `FAILURE_THRESHOLD`: El número máximo de intentos fallidos antes de que se active el Circuit Breaker. En este caso vamos a setear este atributo en 2.
    - `RECOVERY_TIMEOUT`: El tiempo en segundos antes de volver a intentar después de que se haya activado el Circuit Breaker. Pondremos 19 segundos.
    - `EXPECTED_EXCEPTION`: Las excepciones que se consideran fallas para el Circuit Breaker. Probaremos algunos errores de conexión a la API. Aquí podriamos colocar otros errores que el circuit breaker debería de capturar.
    
4. **Definición de la función `call_external_api`**:
    
    ```python
    @MyCircuitBreaker()
    def call_external_api():
        BASE_URL = "<https://6iqdf9i7w9.execute-api.us-east-1.amazonaws.com/dev>"
        END_POINT = "dev"
        resp = requests.get(f"{BASE_URL}/{END_POINT}")
        resp.raise_for_status()
        return resp.json()
    
    ```
    
    Esta función hace una solicitud GET a una API externa. Está decorada con `@MyCircuitBreaker()`, lo que significa que está protegida por el Circuit Breaker. Si la solicitud falla (lanza una excepción), el Circuit Breaker lo registrará. Si el número de fallos supera el umbral definido, el Circuit Breaker se activará y bloqueará más intentos por un tiempo.
    
5. **Definición de la función `index`**:
    
    ```python
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
    
    ```
    
    Esta función maneja una solicitud HTTP a la vista `index`. Intenta llamar a `call_external_api` y, si tiene éxito, renderiza una plantilla `index.html` con los datos obtenidos. Si el Circuit Breaker se activa, o si hay cualquier otra excepción, renderiza una plantilla `error.html` con un mensaje de error correspondiente.