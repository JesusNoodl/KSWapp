# api/v1/belts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.exceptions import NotFoundError

router = APIRouter()


@router.get("/", response_model=list[schemas.BeltOut])
def get_belts(db: Session = Depends(get_db)):
    """Get all belts. Public endpoint."""
    return db.query(models.Belt).all()


@router.get("/{belt_id}", response_model=schemas.BeltOut)
def get_belt(belt_id: int, db: Session = Depends(get_db)):
    """Get a belt by ID. Public endpoint."""
    belt = db.query(models.Belt).filter(models.Belt.id == belt_id).first()
    if belt is None:
        raise NotFoundError("Belt", belt_id)
    return belt
