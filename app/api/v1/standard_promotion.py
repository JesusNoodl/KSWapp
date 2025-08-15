# api/v1/belts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from datetime import datetime

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/standard_promote/")
def standard_promotion(person_id: int, location_id: int, promotion_date: datetime, db: Session = Depends(database.get_db)):
    result = crud.standard_promotion(db, person_id, location_id, promotion_date)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Person not found")
    elif result == "no_rank":
        raise HTTPException(status_code=400, detail="Person has no rank to promote from")
    elif result == "max_rank":
        raise HTTPException(status_code=400, detail="Person already at maximum rank")

    return result