# Django Circuit Breaker Implementation

Este proyecto demuestra cómo implementar un `Circuit Breaker` en una aplicación Django para gestionar llamadas a una API externa de manera robusta. El objetivo es proteger la aplicación de fallos recurrentes en la API, permitiendo un manejo controlado de errores.

## Descripción de la Prueba

La prueba consiste en desplegar una aplicación Django que realiza solicitudes a una API implementada en AWS Lambda. La función Lambda se expone a través de API Gateway, y la aplicación Django utiliza un `Circuit Breaker` para manejar errores de conexión a la API de manera eficiente.

## Objetivos

- **Implementar y configurar un `Circuit Breaker`**: Garantizar que la aplicación sea resistente a fallos repetidos de la API externa.
- **Desplegar una función Lambda**: Utilizar AWS Lambda para alojar la API externa y exponerla a través de API Gateway.
- **Validar la robustez de la aplicación**: Comprobar que el `Circuit Breaker` funcione correctamente bajo condiciones de fallo.

## Pasos para la Implementación

### 1. Desplegar la Función Lambda

1. **Crear la función Lambda**:
    - Desarrolla la función Lambda en Python, que será la API a la que se realizará la llamada.
    - Empaqueta la función Lambda y sus dependencias en un archivo `app.zip`.

2. **Desplegar en AWS**:
    - Sube el archivo `app.zip` a AWS Lambda.
    - Configura la función Lambda con los permisos necesarios.

3. **Configurar API Gateway**:
    - Crea un nuevo API Gateway.
    - Configura un endpoint que apunte a la función Lambda desplegada.
    - Asigna la URL pública generada por API Gateway.

### 2. Configurar la Aplicación Django

1. **Instalar dependencias**:
    - Clona este repositorio y sigue los pasos en la sección de instalación.

2. **Configurar las variables de entorno**:
    - Actualiza la URL base en el código Django (`BASE_URL`) con la URL de la API Gateway.

3. **Desplegar la aplicación Django**:
    - Utiliza `python manage.py runserver` para ejecutar la aplicación localmente o despliega en un servidor de producción.

### 3. Pruebas de la Aplicación

1. **Simulación de errores**:
    - Intencionalmente, cambia la URL en `BASE_URL` para que apunte a un endpoint incorrecto y observe el comportamiento del `Circuit Breaker`.
    - Realiza varias solicitudes a la API para verificar que el `Circuit Breaker` se active tras los fallos configurados.

2. **Monitoreo de logs**:
    - Revisa los logs para asegurarte de que los errores y las activaciones del `Circuit Breaker` se registren correctamente.

## Tecnologías

- **Lenguajes**:
    - Python 3.8+
    - JavaScript (para el frontend en Django)
- **Frameworks**:
    - Django 3.2+ (para la aplicación web)
    - AWS Lambda (para la API en la nube)
- **Librerías**:
    - `requests`: Para realizar llamadas HTTP en Python.
    - `circuitbreaker`: Para implementar el patrón de diseño `Circuit Breaker`.
    - `logging`: Para gestionar los logs en la aplicación Django.
- **Servicios en la nube**:
    - AWS Lambda
    - API Gateway

## Resultados

Al finalizar la implementación:

- La aplicación Django es capaz de realizar llamadas a la API externa de manera confiable.
- El `Circuit Breaker` se activa correctamente después de un número determinado de fallos, protegiendo la aplicación de intentos fallidos repetidos.
- Los errores y eventos críticos se registran en los logs para un monitoreo efectivo.

## Conclusiones

- El uso de un `Circuit Breaker` es fundamental para construir aplicaciones resilientes, especialmente cuando dependen de servicios externos que pueden fallar.
- AWS Lambda, combinado con API Gateway, proporciona una manera eficiente y escalable de desplegar y consumir APIs en la nube.
- La integración de Django con servicios externos puede manejarse de manera robusta utilizando patrones de diseño como `Circuit Breaker`, mejorando la estabilidad y confiabilidad de la aplicación en producción.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
