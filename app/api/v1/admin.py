import requests
import os
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.security import get_current_user  # from earlier JWT logic
from app import crud, database
from sqlalchemy.orm import Session

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")  # e.g. https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def update_user_role(user_id: str, roles: list[str]):
    url = f"{SUPABASE_PROJECT_URL}/auth/v1/admin/users/{user_id}"
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    body = {"app_metadata": {"roles": roles}}

    response = requests.patch(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()

router = APIRouter()

@router.post("/promote")
def promote_user(email: str, new_role: str, current_user=Depends(get_current_user),  db: Session = Depends(database.get_db)):
    # Only admins can promote
    if "admin" not in current_user["roles"]:
        raise HTTPException(status_code=403, detail="Admins only")

    user_id = crud.get_uuid_from_email(db, email)

    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    return update_user_role(str(user_id), [new_role])

@router.get("/uuid/{email}")
def get_user_uuid(email: str, current_user=Depends(get_current_user),  db: Session = Depends(database.get_db)):
    # Only admins can fetch user UUID
    if "admin" not in current_user["roles"]:
        raise HTTPException(status_code=403, detail="Admins only")

    return crud.get_uuid_from_email(db, email)