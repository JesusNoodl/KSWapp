# api/v1/age_category.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.exceptions import NotFoundError

router = APIRouter()


@router.get("/", response_model=list[schemas.AgeCategoryOut])
def get_age_categories(db: Session = Depends(get_db)):
    """Get all age categories. Public endpoint."""
    return db.query(models.AgeCategory).all()


@router.get("/{age_category_id}", response_model=schemas.AgeCategoryOut)
def get_age_category(age_category_id: int, db: Session = Depends(get_db)):
    """Get an age category by ID. Public endpoint."""
    age_category = db.query(models.AgeCategory).filter(
        models.AgeCategory.id == age_category_id
    ).first()
    if age_category is None:
        raise NotFoundError("Age category", age_category_id)
    return age_category
