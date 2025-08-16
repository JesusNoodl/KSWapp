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