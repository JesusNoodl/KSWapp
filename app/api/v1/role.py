# api/v1/role.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.api.v1.auth import require_roles
from app.exceptions import NotFoundError

router = APIRouter()


@router.get("/", response_model=list[schemas.RoleOut])
def get_roles(
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """Get all roles. Requires instructor, admin, or service role."""
    return db.query(models.Role).all()


@router.get("/{role_id}", response_model=schemas.RoleOut)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get a role by ID. Public endpoint."""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise NotFoundError("Role", role_id)
    return role
