from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

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

def test_get_classes():
    response = client.get("/class/")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_class():
    response = client.get("/class/1")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_class_not_found():
    response = client.get("/class/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Class not found"
