# api/v1/role.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from app.database import get_db
from app.api.v1.dependencies import get_current_user
from app.crud import get_user_by_email

router = APIRouter()

# Get all roles
@router.get("/", response_model=list[schemas.RoleOut])
def get_roles(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role not in ["instructor", "admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(models.Role).all()

# Get role
@router.get("/{role_id}", response_model=schemas.RoleOut)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role