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
    # service key bypass
    if token == os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
        return {"role": "service"}
    
    # normal user check
    resp = requests.get(f"{SUPABASE_URL}/auth/v1/user", headers={"Authorization": f"Bearer {token}"})
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return resp.json()


