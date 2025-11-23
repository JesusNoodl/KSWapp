# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import requests
from dotenv import load_dotenv
import os
from app.database import get_db

security = HTTPBearer()
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print(f"Received token (first 20 chars): {token[:20] if token else 'None'}")
    
    # service key bypass
    if token == os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
        print("Service role authenticated")
        return {"role": "service"}
    
    # normal user check
    supabase_url = SUPABASE_URL
    auth_url = f"{supabase_url}/auth/v1/user"
    print(f"Verifying user token with Supabase at: {auth_url}")
    
    resp = requests.get(
        auth_url,
        headers={
            "Authorization": f"Bearer {token}",
            "apikey": os.getenv("SUPABASE_ANON_KEY")
        }
    )
    
    print(f"Supabase auth response status: {resp.status_code}")
    
    if resp.status_code != 200:
        print(f"Auth failed. Response: {resp.text}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_data = resp.json()
    print(f"User authenticated: {user_data.get('email')}")
    return user_data


def get_user_role(
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
) -> str:
    """
    Helper dependency to get the user's role from the database.
    Returns 'service', 'admin', or 'user'.
    """
    # Service role bypass
    if current_user.get("role") == "service":
        return "service"
    
    # Regular user - fetch role from database
    from app.crud import get_user_by_email  # Import here to avoid circular imports
    user = get_user_by_email(db, current_user["email"])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.role