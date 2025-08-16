from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_class():
    response = client.post("/person/enroll", json={
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