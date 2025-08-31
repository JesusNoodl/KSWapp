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
def test_standard_promotion(): 
    payload = {
        "person_id": 15,
        "location_id": 1,
        "promotion_date": "2025-05-02T00:00:00"
    }
    response = client.post("/promotions/standard_promotions/", json=payload)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()


def test_tab_promotion(): 
    payload = {
        "person_id": 15,
        "location_id": 1,
        "promotion_date": "2025-05-03T00:00:00"
    }
    response = client.post("/promotions/tab_promotions/", json=payload)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()

def test_set_belt():
    payload = {
        "person_id": 15,
        "location_id": 1,
        "promotion_date": "2025-05-04T00:00:00",
        "belt_id": 2,
        "tabs": 3
    }
    response = client.post("/promotions/set_belt/", json=payload)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()

def test_delete_promotion():
    response = client.delete("/promotions/delete_promotion/10")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
'''

def test_get_promotions(service_headers):
    response = client.get("/promotions/", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_promotions_for_student(service_headers):
    response = client.get("/promotions/student/15", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_promotion_for_student(service_headers):
    response = client.get("/promotions/student/15/promotion/8", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()




