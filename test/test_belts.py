from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

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

def test_get_belts():
    response = client.get("/belts/")
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

def test_get_belt():
    response = client.get("/belts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "is_stripe" in data
    assert "korean_name" in data
    assert "primary_colour" in data

def test_get_belt_not_found():
    response = client.get("/belts/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Belt not found"


