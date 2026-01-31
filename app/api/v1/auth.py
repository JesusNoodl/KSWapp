# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import requests
from dotenv import load_dotenv
import os
from typing import Callable
from app.database import get_db
from app.exceptions import NotFoundError, ForbiddenError, UnauthorizedError

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
        raise NotFoundError("User")

    return user.role


def require_roles(*allowed_roles: str) -> Callable:
    """
    Dependency factory that creates a role-checking dependency.

    Usage:
        @router.post("/")
        def create_something(
            db: Session = Depends(get_db),
            user_role: str = Depends(require_roles("admin", "instructor"))
        ):
            ...

    Args:
        *allowed_roles: Variable number of role strings that are permitted.
                       Common roles: "service", "admin", "instructor", "user"

    Returns:
        A dependency function that validates the user's role and returns it.

    Raises:
        NotFoundError: If the user is not found in the database.
        ForbiddenError: If the user's role is not in the allowed roles.
    """
    def role_checker(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> str:
        # Service role bypass
        if current_user.get("role") == "service":
            if "service" in allowed_roles:
                return "service"
            raise ForbiddenError()

        # Regular user - fetch role from database
        from app.crud import get_user_by_email  # Import here to avoid circular imports
        user = get_user_by_email(db, current_user["email"])

        if not user:
            raise NotFoundError("User")

        if user.role not in allowed_roles:
            raise ForbiddenError()

        return user.role

    return role_checker


def get_current_user_with_db(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> tuple[dict, any]:
    """
    Returns both the current_user dict and the database user object.
    Useful when you need both the Supabase user info and the database user.

    Returns:
        Tuple of (current_user dict, database User object or None for service)
    """
    if current_user.get("role") == "service":
        return current_user, None

    from app.crud import get_user_by_email
    user = get_user_by_email(db, current_user["email"])

    if not user:
        raise NotFoundError("User")

    return current_user, user