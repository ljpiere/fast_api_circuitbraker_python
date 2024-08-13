import pytest
from fastapi.testclient import TestClient
import requests  # Asegúrate de importar requests
from fast_api_circuitbreaker_python.other_code.fastapi_app import app, MyCircuitBreaker, call_external

client = TestClient(app)

def test_call_external_success(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"name": "Tatooine"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    response = call_external()
    assert response["name"] == "Tatooine"

def test_call_external_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.ConnectionError("Unable to connect")

    monkeypatch.setattr("requests.get", mock_get)

    with pytest.raises(requests.ConnectionError):
        call_external()

def test_circuit_breaker():
    breaker = MyCircuitBreaker()

    for _ in range(MyCircuitBreaker.FAILURE_THRESHOLD):
        with pytest.raises(requests.ConnectionError):
            breaker.call(call_external)

    assert breaker.current_state == "open"

    # Intentar hacer otra llamada debería dar un error CircuitBreakerError
    with pytest.raises(circuitbreaker.CircuitBreakerError):
        breaker.call(call_external)

def test_fastapi_endpoint_success(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"name": "Tatooine"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "Tatooine"

def test_fastapi_endpoint_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.ConnectionError("Unable to connect")

    monkeypatch.setattr("requests.get", mock_get)
    
    response = client.get("/")
    assert response.status_code == 200

