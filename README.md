# Django API Consumer with Circuit Breaker

This Django project demonstrates how to create a web application that consumes an external API (in this case, an AWS API) and implements a circuit breaker pattern. The circuit breaker helps to prevent repeated failed calls to the API by temporarily stopping the requests when the external service is unavailable.

## Table of Contents

- [Installation](#installation)
- [Project Setup](#project-setup)
- [Creating the Circuit Breaker](#creating-the-circuit-breaker)
- [Building the Django Views](#building-the-django-views)
- [Creating the HTML Templates](#creating-the-html-templates)
- [Testing the Application](#testing-the-application)
- [Notes](#notes)

## Installation

Before you begin, make sure you have Python installed on your system. Then, follow these steps to install the necessary dependencies.

1. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
    ```

2. **Install Django and required libraries:**

    ```bash
    pip install Django circuitbreaker requests
    ```

## Project Setup

1. **Create a Django project:**

    ```bash
    django-admin startproject myproject
    cd myproject
    ```

2. **Create a Django app:**

    ```bash
    django-admin startapp myapp
    ```

3. **Update the `settings.py` to include the app:**

    ```python
    # myproject/settings.py

    INSTALLED_APPS = [
        ...
        'myapp',
    ]
    ```

## Creating the Circuit Breaker

We'll use the `circuitbreaker` Python library to implement the circuit breaker pattern in Django.

1. **Define the circuit breaker class and function to call the external API in `views.py`:**

    ```python
    # myapp/views.py

    from django.shortcuts import render
    from circuitbreaker import CircuitBreaker, CircuitBreakerError
    import requests
    import logging

    logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
    logger = logging.getLogger()

    class MyCircuitBreaker(CircuitBreaker):
        FAILURE_THRESHOLD = 5  # Number of failures before the circuit breaker activates
        RECOVERY_TIMEOUT = 60  # Time in seconds before the circuit breaker allows new attempts
        EXPECTED_EXCEPTION = requests.exceptions.RequestException  # Capture all requests exceptions

    @MyCircuitBreaker()
    def call_external_api():
        BASE_URL = "https://6iqdf9i7w9.execute-api.us-east-1.amazonaws.com/dev"
        END_POINT = "dev"
        try:
            resp = requests.get(f"{BASE_URL}/{END_POINT}")
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to the API: {e}")
            raise
    ```

## Building the Django Views

2. **Create the view that handles API requests and renders the response in `views.py`:**

    ```python
    # myapp/views.py

    def index(request):
        try:
            data = call_external_api()
            return render(request, "index.html", {"data": data})
        except CircuitBreakerError:
            message = "Repeated request failures. The Circuit Breaker has been activated to prevent further attempts temporarily."
            return render(request, "error.html", {"message": message, "circuit_breaker": True}, status=503)
        except Exception as e:
            message = f"An error occurred while trying to connect to the API: {str(e)}"
            return render(request, "error.html", {"message": message, "circuit_breaker": False}, status=503)
    ```

3. **Configure the URL routing:**

    - **In `urls.py` of the app:**

        ```python
        # myapp/urls.py

        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.index, name='index'),
        ]
        ```

    - **In `urls.py` of the project:**

        ```python
        # myproject/urls.py

        from django.contrib import admin
        from django.urls import include, path

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('myapp.urls')),
        ]
        ```

## Creating the HTML Templates

4. **Create the HTML templates to display data or error messages:**

    - **`index.html`:**

        ```html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Data from API</title>
        </head>
        <body>
            <h1>Data from API</h1>
            <pre>{{ data | safe }}</pre>
        </body>
        </html>
        ```

    - **`error.html`:**

        ```html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error</title>
        </head>
        <body>
            <h1>Request Error</h1>
            <p>{{ message }}</p>
            {% if circuit_breaker %}
            <p><strong>Note:</strong> This error was caused by the activation of the <strong>Circuit Breaker</strong>. The external API has failed repeatedly, and connection attempts have been temporarily halted to protect the system.</p>
            {% else %}
            <p>An unexpected error occurred. Please try again later.</p>
            {% endif %}
        </body>
        </html>
        ```

## Testing the Application

5. **Run the Django development server:**

    ```bash
    python manage.py runserver
    ```

6. **Test the application:**

    - **Normal Operation:** When the external API is available, you should see the data returned by the API on the `index.html` page.
    - **Circuit Breaker Activation:** Simulate the API being down (e.g., by turning off the API). After the defined number of failures (`FAILURE_THRESHOLD`), the circuit breaker will activate, and you should see the error message indicating that the circuit breaker has been triggered.

## Notes

- The `FAILURE_THRESHOLD` in `MyCircuitBreaker` is set to 5 by default, meaning the circuit breaker will activate after 5 consecutive failures.
- The `RECOVERY_TIMEOUT` is the time (in seconds) after which the circuit breaker will allow new attempts to connect to the API.
- Adjust these values according to your application's needs.

This project is a simple demonstration of how to integrate a circuit breaker into a Django application. For production use, consider additional error handling, logging, and monitoring strategies to ensure the robustness of your application.
