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

@router.get("/{person_id}", response_model=schemas.PersonOut)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.get("/", response_model=list[schemas.PersonOut])
def get_all_people(db: Session = Depends(get_db)):
    return db.query(models.Person).all()
