from fastapi import Depends, HTTPException, status
from jose import jwt
import httpx
from fastapi.security import OAuth2PasswordBearer

SUPABASE_PROJECT_ID = "your-project-ref"
SUPABASE_JWKS_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/jwks"

_jwks = None

async def get_jwks():
    global _jwks
    if not _jwks:
        async with httpx.AsyncClient() as client:
            resp = await client.get(SUPABASE_JWKS_URL)
            resp.raise_for_status()
            _jwks = resp.json()
    return _jwks


async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    jwks = await get_jwks()
    try:
        payload = jwt.decode(token, jwks, algorithms=["RS256"], options={"verify_aud": False})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def require_role(allowed_roles: list[str]):
    """
    Factory that returns a dependency function.
    Example: @app.get("/admin", dependencies=[Depends(require_role(["admin"]))])
    """
    async def role_checker(user=Depends(get_current_user)):
        # Look at role claims in the JWT
        roles = []
        if "role" in user:
            roles.append(user["role"])
        if "app_metadata" in user and "roles" in user["app_metadata"]:
            roles.extend(user["app_metadata"]["roles"])

        if not any(r in allowed_roles for r in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role(s): {allowed_roles}"
            )
        return user
    return role_checker
