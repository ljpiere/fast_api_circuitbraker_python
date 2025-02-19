from fastapi import FastAPI
import requests
import logging

app = FastAPI()
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S %z', level=logging.INFO)
logger = logging.getLogger()

def call_external():
  BASE_URL = "https://swap1.dev"
  END_POINT = "api/planets/1/"
  resp = requests.get(f"{BASE_URL}/{END_POINT}")
  data = []
  if resp.status_code == 200:
    data = resp.json()
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
  except requests.exceptions.ConnectionError as e:
    return {
      "status_code": 500,
      "success": False,
      "message": f"Failed get starwars data: {e}"
    }