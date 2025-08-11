from fastapi.testclient import TestClient
from KSWapp.main import app

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
    print(data)


