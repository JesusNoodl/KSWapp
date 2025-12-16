from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.auth import get_current_user
from app.database import get_db
from app.crud import get_user_by_email, update_user_role

router = APIRouter()

@router.post("/promote")
def promote_user(email: str, new_role: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Only admins can promote
    current_app_user = get_user_by_email(db, current_user["email"])

    if not current_app_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_app_user.role not in ["admin", "service"]:
        raise HTTPException(status_code=403, detail="Admins only")
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if new_role not in ["user", "instructor", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    updated_user = update_user_role(db, user.id, new_role)
    if updated_user == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found", "email": email}
        )
    
    return {"id": str(updated_user.id), "email": updated_user.email, "role": updated_user.role}
