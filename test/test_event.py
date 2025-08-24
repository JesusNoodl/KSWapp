from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/event/", json={
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

def test_get_events():
    response = client.get("/event/")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_event():
    response = client.get("/event/1")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_event_not_found():
    response = client.get("/event/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Event not found"