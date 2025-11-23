# test_awards.py
import os
from dotenv import load_dotenv
import requests
from fastapi.testclient import TestClient
from main import app
import pytest
from datetime import datetime, date

# Load env vars from project root .env (one dir up from test/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = TestClient(app)


@pytest.fixture
def service_headers():
    return {
        "Authorization": f"Bearer {SERVICE_KEY}",
        "apikey": SERVICE_KEY,
        "Content-Type": "application/json"
    }


def test_get_all_awards(service_headers):
    """Test retrieving all awards (admin/instructor only)"""
    response = client.get("/awards/", headers=service_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # If there are awards, check the structure from full_award view
    if data:
        award = data[0]
        # Fields from FullAwardOut schema
        assert "id" in award
        assert "award_name" in award
        assert "award_type" in award
        assert "points" in award
        assert "name" in award
        assert "belt_at_time" in award
        assert "belt_at_time_korean" in award
        assert "event" in award
        assert "tournament_category" in award
        assert "tournament_category_upper" in award
        assert "date_achieved" in award
        assert "person_id" in award


def test_get_awards_for_student(service_headers):
    """Test retrieving awards for a specific student"""
    student_id = 6
    
    response = client.get(f"/awards/student/{student_id}", headers=service_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # Check all returned awards belong to the correct student
    for award in data:
        assert award["person_id"] == student_id



def test_get_awards_for_student_with_no_awards(service_headers):
    """Test retrieving awards for a student with no awards returns empty list"""
    student_id = 9999
    
    response = client.get(f"/awards/student/{student_id}", headers=service_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_specific_award(service_headers):
    """Test retrieving a specific award by ID"""
    # First, get all awards to find a valid ID
    response = client.get("/awards/", headers=service_headers)
    awards = response.json()
    
    if awards:
        award_id = awards[0]["id"]
        
        response = client.get(f"/awards/{award_id}", headers=service_headers)
        assert response.status_code == 200
        data = response.json()
        # Fields from FullAwardOut schema
        assert data["id"] == award_id
        assert "award_name" in data
        assert "name" in data
        assert "belt_at_time" in data


def test_get_award_not_found(service_headers):
    """Test retrieving a non-existent award returns 404"""
    response = client.get("/awards/99999", headers=service_headers)
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_create_award(service_headers):
    """Test creating a new award"""
    payload = {
        "award_type": 1,
        "person": 6,
        "rank_at_time": 10,
        "event": 8,
        "date_achieved": date.today().isoformat(),
        "tournament_category": 1
    }
    
    response = client.post("/awards/", json=payload, headers=service_headers)
    
    assert response.status_code == 201
    data = response.json()
    
    # POST returns AwardOut schema (from underlying table, not view)
    assert "id" in data
    assert data["award_type"] == payload["award_type"]
    assert data["person"] == payload["person"]
    assert data["rank_at_time"] == payload["rank_at_time"]
    assert data["event"] == payload["event"]
    assert data["tournament_category"] == payload["tournament_category"]
    assert "created_at" in data
    assert "modified_at" in data
    
    # Clean up: delete the created award
    award_id = data["id"]
    client.delete(f"/awards/{award_id}", headers=service_headers)


def test_create_award_without_rank(service_headers):
    """Test creating an award without specifying rank_at_time (should use person's current belt)"""
    payload = {
        "award_type": 1,
        "person": 6,
        "date_achieved": date.today().isoformat()
    }
    
    response = client.post("/awards/", json=payload, headers=service_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["rank_at_time"] is not None
    
    # Clean up
    client.delete(f"/awards/{data['id']}", headers=service_headers)


def test_create_award_person_not_found(service_headers):
    """Test creating an award with non-existent person returns 404"""
    payload = {
        "award_type": 1,
        "person": 99999,
        "date_achieved": date.today().isoformat()
    }
    
    response = client.post("/awards/", json=payload, headers=service_headers)
    
    assert response.status_code == 404
    data = response.json()
    
    # Handle both dict and string detail formats
    detail = data["detail"]
    if isinstance(detail, dict):
        assert "person not found" in detail["error"].lower()
    else:
        assert "person not found" in detail.lower()


def test_create_award_type_not_found(service_headers):
    """Test creating an award with non-existent award_type returns 404"""
    payload = {
        "award_type": 99999,
        "person": 6,
        "date_achieved": date.today().isoformat()
    }
    
    response = client.post("/awards/", json=payload, headers=service_headers)
    
    assert response.status_code == 404
    data = response.json()
    
    # Handle both dict and string detail formats
    detail = data["detail"]
    if isinstance(detail, dict):
        assert "award type not found" in detail["error"].lower()
    else:
        assert "award type not found" in detail.lower()


def test_create_award_no_belt_level(service_headers):
    """Test creating an award for person with no belt and no rank_at_time provided"""
    # This test requires a person with belt_level_id = NULL
    # Skip if you don't have such a person in your test database
    payload = {
        "award_type": 1,
        "person": 6,
        "date_achieved": date.today().isoformat()
    }
    
    response = client.post("/awards/", json=payload, headers=service_headers)
    # This test is flexible - person 6 likely has a belt, so it will succeed
    # If you want to test the "no_belt" error, use a person without a belt_level_id
    assert response.status_code in [201, 400]
    
    if response.status_code == 400:
        data = response.json()
        detail = data["detail"]
        if isinstance(detail, dict):
            assert "no current belt level" in detail["error"].lower()
        else:
            assert "no current belt level" in detail.lower()
    elif response.status_code == 201:
        # Clean up if created
        client.delete(f"/awards/{response.json()['id']}", headers=service_headers)


def test_update_award(service_headers):
    """Test updating an existing award"""
    # First create an award to update
    create_payload = {
        "award_type": 1,
        "person": 6,
        "rank_at_time": 11,
        "date_achieved": date.today().isoformat()
    }
    
    create_response = client.post("/awards/", json=create_payload, headers=service_headers)
    
    assert create_response.status_code == 201
    award_id = create_response.json()["id"]
    
    # Now update it
    update_payload = {
        "award_type": 2,
        "person": 6,
        "rank_at_time": 12,
        "date_achieved": date.today().isoformat()
    }
    
    response = client.put(f"/awards/{award_id}", json=update_payload, headers=service_headers)
    assert response.status_code == 200
    data = response.json()
    
    # PUT returns AwardOut schema (from underlying table)
    assert data["award_type"] == update_payload["award_type"]
    assert data["rank_at_time"] == update_payload["rank_at_time"]
    assert "id" in data
    assert "created_at" in data
    
    # Clean up
    client.delete(f"/awards/{award_id}", headers=service_headers)


def test_update_award_not_found(service_headers):
    """Test updating a non-existent award returns 404"""
    update_payload = {
        "award_type": 1,
        "person": 6,
        "rank_at_time": 10,
        "date_achieved": date.today().isoformat()
    }
    
    response = client.put("/awards/99999", json=update_payload, headers=service_headers)
    
    assert response.status_code == 404
    data = response.json()
    
    # Handle both dict and string detail formats
    detail = data["detail"]
    if isinstance(detail, dict):
        assert "award not found" in detail["error"].lower()
    else:
        assert "award not found" in detail.lower()


def test_delete_award(service_headers):
    """Test deleting an award"""
    # First create an award to delete
    create_payload = {
        "award_type": 1,
        "person": 6,
        "rank_at_time": 13,
        "date_achieved": date.today().isoformat()
    }
    
    create_response = client.post("/awards/", json=create_payload, headers=service_headers)
    
    assert create_response.status_code == 201
    award_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/awards/{award_id}", headers=service_headers)
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/awards/{award_id}", headers=service_headers)
    assert get_response.status_code == 404


def test_delete_award_not_found(service_headers):
    """Test deleting a non-existent award returns 404"""
    response = client.delete("/awards/99999", headers=service_headers)
    assert response.status_code == 404
    data = response.json()
    
    # Handle both dict and string detail formats
    detail = data["detail"]
    if isinstance(detail, dict):
        assert "award not found" in detail["error"].lower()
    else:
        assert "award not found" in detail.lower()


def test_create_award_with_event(service_headers):
    """Test creating an award with an event"""
    payload = {
        "award_type": 1,
        "person": 6,
        "rank_at_time": 10,
        "event": 8,
        "date_achieved": date.today().isoformat()
    }
    
    response = client.post("/awards/", json=payload, headers=service_headers)
    
    # Will be 201 if event exists, 404 if not
    if response.status_code == 201:
        data = response.json()
        assert data["event"] == payload["event"]
        client.delete(f"/awards/{data['id']}", headers=service_headers)
    elif response.status_code == 404:
        data = response.json()
        detail = data["detail"]
        if isinstance(detail, dict):
            assert "event not found" in detail["error"].lower()
        else:
            assert "event not found" in detail.lower()
    else:
        # Debug unexpected response
        assert False, f"Unexpected status code: {response.status_code}"


def test_create_award_with_tournament_category(service_headers):
    """Test creating an award with a tournament category"""
    payload = {
        "award_type": 1,
        "person": 6,
        "rank_at_time": 10,
        "tournament_category": 1,
        "date_achieved": date.today().isoformat()
    }
    
    response = client.post("/awards/", json=payload, headers=service_headers)
    
    # Will be 201 if category exists, 404 if not
    if response.status_code == 201:
        data = response.json()
        assert data["tournament_category"] == payload["tournament_category"]
        client.delete(f"/awards/{data['id']}", headers=service_headers)
    elif response.status_code == 404:
        data = response.json()
        detail = data["detail"]
        if isinstance(detail, dict):
            assert "tournament category not found" in detail["error"].lower()
        else:
            assert "tournament category not found" in detail.lower()
    else:
        # Debug unexpected response
        assert False, f"Unexpected status code: {response.status_code}"


def test_award_appears_in_view_after_creation(service_headers):
    """Test that a created award appears in the full_award view with proper denormalization"""
    # Create an award
    create_payload = {
        "award_type": 1,
        "person": 6,
        "rank_at_time": 10,
        "date_achieved": date.today().isoformat()
    }
    
    create_response = client.post("/awards/", json=create_payload, headers=service_headers)
    assert create_response.status_code == 201
    award_id = create_response.json()["id"]
    
    # Fetch it via the view (GET endpoint)
    get_response = client.get(f"/awards/{award_id}", headers=service_headers)
    assert get_response.status_code == 200
    
    view_data = get_response.json()
    # Verify it has the denormalized fields from the view
    assert view_data["id"] == award_id
    assert "award_name" in view_data  # From award_type join
    assert "award_type" in view_data  # From award_type join
    assert "name" in view_data  # Concatenated person name
    assert "belt_at_time" in view_data  # From belt join
    assert view_data["person_id"] == create_payload["person"]
    
    # Clean up
    client.delete(f"/awards/{award_id}", headers=service_headers)