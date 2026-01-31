# api/v1/location.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.api.v1.auth import require_roles
from app.exceptions import NotFoundError

router = APIRouter()


@router.post("/", response_model=schemas.LocationOut)
def create_location(
    location: schemas.LocationCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """Create a new location. Requires admin or service role."""
    return crud.create_location(db, location)


@router.get("/", response_model=list[schemas.LocationOut])
def get_locations(db: Session = Depends(get_db)):
    """Get all locations. Public endpoint."""
    return db.query(models.Location).all()


@router.get("/{location_id}", response_model=schemas.LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Get a location by ID. Public endpoint."""
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if location is None:
        raise NotFoundError("Location", location_id)
    return location
