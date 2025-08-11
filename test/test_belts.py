# tests/test_belts.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_belt():
    payload = {
        "name": "blue stripe belt",
        "is_stripe": False,
        "korean_name": "XXX",
        "primary_colour": "yellow"
    }
    response = client.post("/belts/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "blue stripe belt"
    assert data["primary_colour"] == "yellow"
