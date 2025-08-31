# api/v1/class.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from app.database import get_db
from app.api.v1.dependencies import get_current_user
from app.crud import get_user_by_email

router = APIRouter()

# Create a new class
@router.post("/", response_model=schemas.ClassOut)
def create_class(class_: schemas.ClassCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role not in ["admin", "service"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.create_class(db, class_)

# Get a class by ID
@router.get("/{class_id}", response_model=schemas.ClassOut)
def get_class(class_id: int, db: Session = Depends(get_db)):
    class_ = db.query(models.Class).filter(models.Class.id == class_id).first()
    if class_ is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

# Get all classes
@router.get("/", response_model=list[schemas.ClassOut])
def get_all_classes(db: Session = Depends(get_db)):
    return db.query(models.Class).all()

@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(get_current_user)
):
    # If service role, skip email lookup
    if current_user.get("role") == "service":
        user_role = "service"
    else:
        # regular user, fetch from db
        user = get_user_by_email(db, current_user["email"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_role = user.role

    if user_role not in ["admin", "service"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = crud.delete_class(db, class_id)

    if result == "not_found":
        raise HTTPException(
            status_code=404,
            detail={"error": "Class not found", "class_id": class_id}
        )

    return {"status": "success", "deleted_class": result}


# Edit a class
@router.put("/{class_id}", response_model=schemas.ClassOut)
def update_class(class_id: int, class_: schemas.ClassUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role not in ["admin", "service"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.update_class(db, class_id, class_)
