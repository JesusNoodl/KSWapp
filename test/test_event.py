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
def test_create_event(service_headers):
    response = client.post("/event/", headers=service_headers, json={
        "title": "test event",
        "description": "this is a test event",
        "event_date": "2025-10-15T00:00:00Z",
        "start_time": "08:00:00",
        "end_time": "11:00:00",
        "location_id": 3,
        "age_categories": [2, 3, 4, 5],
        "event_type_id": 3
    })
    assert response.status_code == 200
    assert response.json()["title"] == "test event"
    assert response.json()["description"] == "this is a test event"
    assert response.json()["event_date"] == "2025-10-15T00:00:00Z"
    assert response.json()["start_time"] == "08:00:00"
    assert response.json()["end_time"] == "11:00:00"
    assert response.json()["location_id"] == 3
    assert response.json()["event_type_id"] == 3
    data = response.json()
    print("\nDEBUG Create Event Response JSON:", data)
'''
def test_get_events(service_headers):
    response = client.get("/event/", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_event(service_headers):
    response = client.get("/event/1", headers=service_headers)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_event_not_found(service_headers):
    response = client.get("/event/9999", headers=service_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Event not found"