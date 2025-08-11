from fastapi.testclient import TestClient
from KSWapp.main import app

client = TestClient(app)

def test_create_belt():
    payload = {
        "name": "blue belt",
        "is_stripe": False,
        "korean_name": "XXX",
        "primary_colour": "blue"
    }
    response = client.post("/belts/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "blue belt"
    assert data["primary_colour"] == "blue"
