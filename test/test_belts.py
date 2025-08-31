import os
from dotenv import load_dotenv
import requests
from fastapi.testclient import TestClient
from main import app
import pytest

# Load env vars from project root .env (one dir up from test/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = TestClient(app)

@pytest.fixture
def service_headers():
    return {
        "Authorization": f"Bearer {SERVICE_KEY}",
        "apikey": SERVICE_KEY,  # include api key if your backend expects it
        "Content-Type": "application/json"
    }

'''
def test_create_belt():
    payload = {
        "name": "red stripe belt",
        "is_stripe": True,
        "korean_name": "XXX",
        "primary_colour": "blue"
    }
    response = client.post("/belts/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "red stripe belt"
    assert data["primary_colour"] == "blue"
'''

def test_get_belts(service_headers):
    response = client.get("/belts/", headers=service_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]
        assert "name" in data[0]
        assert "is_stripe" in data[0]
        assert "korean_name" in data[0]
        assert "primary_colour" in data[0]
    print(data)

def test_get_belt(service_headers):
    response = client.get("/belts/1", headers=service_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "is_stripe" in data
    assert "korean_name" in data
    assert "primary_colour" in data

def test_get_belt_not_found(service_headers):
    response = client.get("/belts/9999", headers=service_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Belt not found"


