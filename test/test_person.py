from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
'''
def test_enroll_student():
    response = client.post("/person/enroll", json={
        "first_name": "James",
        "last_name": "Willems",
        "dob": "1987-10-15T00:00:00Z",
        "age_category_id": 5
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "James"
    assert response.json()["last_name"] == "Willems"
    assert response.json()["dob"] == "1987-10-15T00:00:00Z"
    assert response.json()["age_category_id"] == 5
    data = response.json()
    print("\nDEBUG Enroll Student Response JSON:", data)
'''

def test_get_persons():
    response = client.get("/person/")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_person():
    response = client.get("/person/7")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 7

def test_get_person_not_found():
    response = client.get("/person/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Person not found"