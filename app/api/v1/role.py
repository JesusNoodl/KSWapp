# api/v1/role.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, models

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all roles
@router.get("/", response_model=list[schemas.RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return db.query(models.Role).all()

# Get role
@router.get("/{role_id}", response_model=schemas.RoleOut)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role