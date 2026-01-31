# api/v1/admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.auth import require_roles
from app.database import get_db
from app.crud import get_user_by_email, update_user_role
from app.exceptions import NotFoundError, BadRequestError

router = APIRouter()


@router.post("/promote")
def promote_user(
    email: str,
    new_role: str,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """Promote a user to a new role. Requires admin or service role."""
    user = get_user_by_email(db, email)
    if not user:
        raise NotFoundError("User", email)

    if new_role not in ["user", "instructor", "admin"]:
        raise BadRequestError(f"Invalid role: {new_role}. Must be one of: user, instructor, admin")

    updated_user = update_user_role(db, user.id, new_role)

    return {"id": str(updated_user.id), "email": updated_user.email, "role": updated_user.role}
