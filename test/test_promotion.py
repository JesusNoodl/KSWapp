from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
'''
def test_standard_promotion(): 
    payload = {
        "person_id": 15,
        "location_id": 1,
        "promotion_date": "2025-05-02T00:00:00"
    }
    response = client.post("/promotions/standard_promotions/", json=payload)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()


def test_tab_promotion(): 
    payload = {
        "person_id": 15,
        "location_id": 1,
        "promotion_date": "2025-05-03T00:00:00"
    }
    response = client.post("/promotions/tab_promotions/", json=payload)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()

def test_set_belt():
    payload = {
        "person_id": 15,
        "location_id": 1,
        "promotion_date": "2025-05-04T00:00:00",
        "belt_id": 2,
        "tabs": 3
    }
    response = client.post("/promotions/set_belt/", json=payload)
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()

def test_delete_promotion():
    response = client.delete("/promotions/delete_promotion/10")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
'''

def test_get_promotions():
    response = client.get("/promotions/")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_promotions_for_student():
    response = client.get("/promotions/student/15")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_promotion_for_student():
    response = client.get("/promotions/student/15/promotion/8")
    print("\nDEBUG Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()




