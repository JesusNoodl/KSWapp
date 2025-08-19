# api/v1/age_category.py
from fastapi import APIRouter, Depends
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