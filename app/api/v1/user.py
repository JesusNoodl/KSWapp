# app/api/v1/user.py
"""
User-specific endpoints for the authenticated user.
This handles getting the current user's role and profile information.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.auth import get_current_user
from app.database import get_db
from app.crud import get_user_by_email
from pydantic import BaseModel

router = APIRouter()


class UserRoleResponse(BaseModel):
    """Response schema for the user role endpoint"""
    email: str
    role: str
    
    class Config:
        from_attributes = True


@router.get("/me/role", response_model=UserRoleResponse)
def get_my_role(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current authenticated user's role.
    
    This endpoint is called by the frontend after login to determine
    what areas of the application the user can access (user, instructor, admin).
    
    Returns:
        UserRoleResponse: The user's email and role
    
    Raises:
        HTTPException 403: If service role tries to access (they should use other endpoints)
        HTTPException 404: If user not found in database
    """
    # Service role shouldn't use this endpoint
    if current_user.get("role") == "service":
        raise HTTPException(
            status_code=403,
            detail="Service role cannot access user-specific endpoints"
        )
    
    # Fetch user from database to get their role
    user = get_user_by_email(db, current_user["email"])
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found in database"
        )
    
    return UserRoleResponse(
        email=user.email,
        role=user.role
    )