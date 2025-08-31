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
def test_create_class():
    response = client.post("/class/", json={
        "title": "test class",
        "description": "this is a test class",
        "day": "Saturday",
        "start_time": "08:00:00",
        "end_time": "11:00:00",
        "location_id": 1,
        "instructor_id": 7,
        "age_categories": [4, 5]
    })
    assert response.status_code == 200
    assert response.json()["title"] == "test class"
    assert response.json()["description"] == "this is a test class"
    assert response.json()["day"] == "Saturday"
    assert response.json()["start_time"] == "08:00:00"
    assert response.json()["end_time"] == "11:00:00"
    assert response.json()["location_id"] == 1
    assert response.json()["instructor_id"] == 7
    data = response.json()
    print("\nDEBUG Create Class Response JSON:", data)

'''

def test_get_classes(service_headers):
    response = client.get("/class/", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_class(service_headers):
    response = client.get("/class/1", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_class_not_found(service_headers):
    response = client.get("/class/9999", headers=service_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Class not found"
'''
def test_delete_class(service_headers):
    response = client.delete("/class/31", headers=service_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["deleted_class"]["id"] == 31
'''
