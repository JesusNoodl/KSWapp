# api/v1/event.py
from fastapi import APIRouter, Depends, HTTPException, status
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

# Create a new event
@router.post("/", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)

# Get an event by ID
@router.get("/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Get all events
@router.get("/", response_model=list[schemas.EventOut])
def get_all_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

# Delete an event
@router.delete("/event/{event_id}")
def delete_event(event_id: int, db: Session = Depends(database.get_db)):
    result = crud.delete_event(db, event_id)

    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Event not found", "event_id": event_id}
        )

    return {"status": "success", "deleted_event": result}