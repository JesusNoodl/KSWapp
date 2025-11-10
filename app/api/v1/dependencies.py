from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
from dotenv import load_dotenv
import os

security = HTTPBearer()

load_dotenv()  # Load environment variables from .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    # Log for debugging (remove in production)
    print(f"Received token (first 20 chars): {token[:20] if token else 'None'}")
    
    # service key bypass
    if token == os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
        print("Service role authenticated")
        return {"role": "service"}
    
    # normal user check
    print(f"Verifying user token with Supabase at: {SUPABASE_URL}/auth/v1/user")
    
    resp = requests.get(
        f"{SUPABASE_URL}/auth/v1/user", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Supabase auth response status: {resp.status_code}")
    
    if resp.status_code != 200:
        print(f"Auth failed. Response: {resp.text}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_data = resp.json()
    print(f"User authenticated: {user_data.get('email')}")
    
    return user_data


