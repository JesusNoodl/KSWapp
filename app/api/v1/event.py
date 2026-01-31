# api/v1/event.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.api.v1.auth import require_roles
from app.exceptions import NotFoundError

router = APIRouter()


@router.post("/", response_model=schemas.EventOut)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """Create a new event. Requires admin or service role."""
    return crud.create_event(db, event)


@router.get("/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get an event by ID. Public endpoint."""
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise NotFoundError("Event", event_id)
    return event


@router.get("/", response_model=list[schemas.EventOut])
def get_all_events(db: Session = Depends(get_db)):
    """Get all events. Public endpoint."""
    return db.query(models.Event).all()


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """Delete an event. Requires admin or service role."""
    result = crud.delete_event(db, event_id)
    return {"status": "success", "deleted_event": result}
