import requests
import os
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.security import get_current_user  # from earlier JWT logic

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
def promote_user(email: str, new_role: str, current_user=Depends(get_current_user)):
    # Only admins can promote
    if "admin" not in current_user["roles"]:
        raise HTTPException(status_code=403, detail="Admins only")

    # Lookup user in Supabase
    # (use supabase-py or REST API to fetch by email -> get user_id)
    user_id = "<fetched-from-supabase>"

    return update_user_role(user_id, [new_role])

