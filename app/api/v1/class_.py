# api/v1/class.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.api.v1.auth import require_roles
from app.exceptions import NotFoundError

router = APIRouter()


@router.post("/", response_model=schemas.ClassOut)
def create_class(
    class_: schemas.ClassCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """Create a new class. Requires admin or service role."""
    return crud.create_class(db, class_)


@router.get("/{class_id}", response_model=schemas.ClassOut)
def get_class(class_id: int, db: Session = Depends(get_db)):
    """Get a class by ID. Public endpoint."""
    class_ = db.query(models.Class).filter(models.Class.id == class_id).first()
    if class_ is None:
        raise NotFoundError("Class", class_id)
    return class_


@router.get("/", response_model=list[schemas.ClassOut])
def get_all_classes(db: Session = Depends(get_db)):
    """Get all active classes. Public endpoint."""
    return db.query(models.Class).filter(models.Class.is_active == True).all()


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """Delete a class. Requires admin or service role."""
    result = crud.delete_class(db, class_id)
    return {"status": "success", "deleted_class": result}


@router.put("/{class_id}", response_model=schemas.ClassOut)
def update_class(
    class_id: int,
    class_: schemas.ClassUpdate,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """Update a class. Requires admin or service role."""
    return crud.update_class(db, class_id, class_)


@router.get("/cancelled", response_model=list[schemas.ClassExceptionOut])
def get_all_class_exceptions(db: Session = Depends(get_db)):
    """Get all class exceptions/cancellations. Public endpoint."""
    return db.query(models.ClassException).all()
