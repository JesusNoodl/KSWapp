# api/v1/person.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from app.api.v1.dependencies import get_current_user
from app.api.v1.admin import get_user_by_email

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Enroll a new student
@router.post("/enroll", response_model=schemas.PersonOut)
def enroll_student(person: schemas.PersonCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role not in ["instructor", "admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.enroll_person(db, person)

# Get a student by ID
@router.get("/{person_id}", response_model=schemas.PersonOut)
def get_person(person_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role not in ["instructor", "admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

# Get all students
@router.get("/", response_model=list[schemas.PersonOut])
def get_all_people(db: Session = Depends(get_db)):
    return db.query(models.Person).all()

# Update a student by ID
@router.put("/{person_id}", response_model=schemas.PersonOut)
def update_person(person_id: int, person_update: schemas.PersonUpdate, db: Session = Depends(get_db)):
    return crud.update_person(db, person_id, person_update)
