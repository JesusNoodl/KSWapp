# api/v1/age_category.py
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

# Get all age categories
@router.get("/", response_model=list[schemas.AgeCategoryOut])
def get_age_categories(db: Session = Depends(get_db)):
    return db.query(models.AgeCategory).all()

# Get age categories
@router.get("/{age_categorie}", response_model=schemas.AgeCategoryOut)
def get_age_categorie(age_categorie: int, db: Session = Depends(get_db)):
    age_category = db.query(models.AgeCategory).filter(models.AgeCategory.id == age_categorie).first()
    if age_category is None:
        raise HTTPException(status_code=404, detail="Age category not found")
    return age_category