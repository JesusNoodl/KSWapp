import pytest
import requests
from fastapi.testclient import TestClient
from main import app  # Adjust if your FastAPI app is elsewhere
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

ADMIN_EMAIL = "max.moxey-hallam@outlook.com"
ADMIN_PASSWORD = "admin123"


client = TestClient(app)


def get_jwt(email: str, password: str) -> str:
    """
    Logs in via Supabase Auth and returns the JWT access_token.
    """
    resp = requests.post(
        f"{DATABASE_URL}/auth/v1/token?grant_type=password",
        headers={
            "apikey": SUPABASE_ANON_KEY,
            "Content-Type": "application/json"
        },
        json={"email": email, "password": password}
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


@pytest.fixture
def admin_token():
    return get_jwt(ADMIN_EMAIL, ADMIN_PASSWORD)


def test_get_person_admin(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/person/7", headers=headers)  
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "first_name" in data  # depends on your PersonOut schema
