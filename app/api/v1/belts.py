# api/belts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .... import crud, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.BeltOut)
def create_belt(belt: schemas.BeltCreate, db: Session = Depends(database.get_db)):
    return crud.create_belt(db, belt)
