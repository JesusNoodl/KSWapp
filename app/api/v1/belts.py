# api/v1/belts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

router = APIRouter()

# Get all belts
@router.get("/", response_model=list[schemas.BeltOut])
def get_belts(db: Session = Depends(get_db)):
    return db.query(models.Belt).all()

# Get one belt by ID
@router.get("/{belt_id}", response_model=schemas.BeltOut)
def get_belt(belt_id: int, db: Session = Depends(get_db)):
    belt = db.query(models.Belt).filter(models.Belt.id == belt_id).first()
    if belt is None:
        raise HTTPException(status_code=404, detail="Belt not found")
    return belt
