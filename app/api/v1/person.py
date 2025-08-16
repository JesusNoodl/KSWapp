# api/v1/person.py
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

@router.post("/enroll", response_model=schemas.PersonOut)
def enroll_student(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.enroll_person(db, person)
