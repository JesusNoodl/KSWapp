# api/v1/belts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from app.database import get_db
from app.api.v1.dependencies import get_current_user
from app.crud import get_user_by_email

router = APIRouter()

# Create a new belt rank
@router.post("/", response_model=schemas.BeltOut)
def create_belt(belt: schemas.BeltCreate, db: Session = Depends(database.get_db), current_user=Depends(get_current_user)):
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role not in ["instructor", "admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
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
