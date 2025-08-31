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
def test_enroll_student():
    response = client.post("/person/enroll", json={
        "first_name": "James",
        "last_name": "Willems",
        "dob": "1987-10-15T00:00:00Z",
        "age_category_id": 5
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "James"
    assert response.json()["last_name"] == "Willems"
    assert response.json()["dob"] == "1987-10-15T00:00:00Z"
    assert response.json()["age_category_id"] == 5
    data = response.json()
    print("\nDEBUG Enroll Student Response JSON:", data)
'''

def test_get_persons(service_headers):
    response = client.get("/person/", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_person(service_headers):
    response = client.get("/person/7", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 7

def test_get_person_not_found(service_headers):
    response = client.get("/person/9999", headers=service_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Person not found"