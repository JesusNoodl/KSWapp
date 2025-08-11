# api/belts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from KSWapp import crud, schemas, database, models

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.BeltOut)
def create_belt(belt: schemas.BeltCreate, db: Session = Depends(database.get_db)):
    return crud.create_belt(db, belt)

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
