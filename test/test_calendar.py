import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app
import pytest
from datetime import date

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

client = TestClient(app)

def test_get_schedule():
    """Test getting the class schedule (no auth required)"""
    response = client.get("/calendar/schedule")
    print("\nDEBUG Schedule Response:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]
        assert "title" in data[0]
        assert "day_number" in data[0]
        assert "start_time" in data[0]

def test_get_calendar_events():
    """Test getting calendar events for a specific month"""
    # Get current month
    today = date.today()
    year = today.year
    month = today.month
    
    response = client.get(f"/calendar/calendar?year={year}&month={month}")
    print("\nDEBUG Calendar Response:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_calendar_events_invalid_month():
    """Test calendar endpoint with invalid month"""
    response = client.get("/calendar/calendar?year=2025&month=13")
    assert response.status_code == 400
    assert "Month must be between 1 and 12" in response.json()["detail"]

def test_get_cancelled_classes():
    """Test getting cancelled classes"""
    response = client.get("/calendar/cancelled-classes")
    print("\nDEBUG Cancelled Classes Response:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)