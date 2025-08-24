# api/v1/class.py
from fastapi import APIRouter, Depends, HTTPException, status
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

# Create a new class
@router.post("/", response_model=schemas.ClassOut)
def create_class(class_: schemas.ClassCreate, db: Session = Depends(get_db)):
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

# Delete a class
@router.delete("/class/{class_id}")
def delete_class(class_id: int, db: Session = Depends(database.get_db)):
    result = crud.delete_class(db, class_id)

    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Class not found", "class_id": class_id}
        )

    return {"status": "success", "deleted_class": result}

    return {"status": "success", "deleted_promotion": result}

