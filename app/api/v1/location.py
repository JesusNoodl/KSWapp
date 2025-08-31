# api/v1/location.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from app.database import get_db
from app.api.v1.dependencies import get_current_user
from app.crud import get_user_by_email

router = APIRouter()

# Create a new location
@router.post("/", response_model=schemas.LocationOut)
def create_location(location: schemas.LocationCreate, db: Session = Depends(database.get_db), current_user=Depends(get_current_user)):
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role not in ["admin", "service"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.create_location(db, location)

# Get all locations
@router.get("/", response_model=list[schemas.LocationOut])
def get_locations(db: Session = Depends(get_db)):
    return db.query(models.Location).all()

# Get location
@router.get("/{location_id}", response_model=schemas.LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location