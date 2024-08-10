# conda activate espbig
from fastapi import FastAPI
import requests
import logging

app = FastAPI()
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

def call_external():
    BASE_URL = "https://swapi.dev"
    END_POINT = "api/planets/1/"
    resp = requests.get(f"{BASE_URL}/{END_POINT}")
    data = []
    if resp.status_code == 200:
        data = resp.json()
    return data

@app.get("/")
def implement_circuit_breaker():
    data = call_external()
    return {
        "status_code": 200,
        "success": True,
        "message": "Success get starwars data",
        "data": data
}