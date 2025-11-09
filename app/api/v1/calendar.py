# app/api/v1/calendar.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter()

# Get all active classes for the schedule page
@router.get("/schedule", response_model=List[schemas.ClassScheduleOut])
def get_schedule(db: Session = Depends(get_db)):
    """
    Get all active classes for the schedule page.
    No authentication required - public information.
    """
    classes = db.query(models.Class).filter(
        models.Class.is_active == True
    ).order_by(
        models.Class.day_number,
        models.Class.start_time
    ).all()
    
    return classes


# Get calendar events for a specific month
@router.get("/calendar", response_model=List[schemas.CalendarEventOut])
def get_calendar_events(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """
    Get all calendar events (classes and events) for a specific month.
    No authentication required - public information.
    
    Parameters:
    - year: Year (e.g., 2025)
    - month: Month (1-12)
    """
    # Validate inputs
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
    
    # Calculate first and last day of the month
    from calendar import monthrange
    _, last_day = monthrange(year, month)
    
    first_date = date(year, month, 1)
    last_date = date(year, month, last_day)
    
    # Query both classes and events separately, then combine
    events = []
    
    # Get recurring classes for the month
    classes = db.query(models.Class).filter(
        models.Class.is_active == True
    ).all()
    
    # Generate dates for each class in the month
    current_date = first_date
    while current_date <= last_date:
        day_of_week = current_date.weekday()  # Monday = 0, Sunday = 6
        
        for class_obj in classes:
            if class_obj.day_number == day_of_week:
                # Check if this class is cancelled on this date
                cancellation = db.query(models.ClassException).filter(
                    models.ClassException.class_id == class_obj.id,
                    models.ClassException.date == current_date,
                    models.ClassException.cancelled == True
                ).first()
                
                if not cancellation:
                    location = db.query(models.Location).filter(
                        models.Location.id == class_obj.location_id
                    ).first()
                    
                    events.append({
                        "id": class_obj.id,
                        "calendar_type": "class",
                        "class_id": class_obj.id,
                        "event_id": None,
                        "class_name": class_obj.title,
                        "description": class_obj.description,
                        "date": str(current_date),
                        "day": class_obj.day,
                        "start_time": str(class_obj.start_time) if class_obj.start_time else None,
                        "end_time": str(class_obj.end_time) if class_obj.end_time else None,
                        "location_name": location.title if location else None,
                        "location_id": class_obj.location_id,
                        "is_dojang": location.is_dojang if location else None,
                        "instructor_id": class_obj.instructor_id,
                        "event_type": None,
                        "day_number": class_obj.day_number,
                    })
        
        current_date += timedelta(days=1)
    
    # Get one-time events for the month
    event_objects = db.query(models.Event).filter(
        models.Event.event_start >= first_date,
        models.Event.event_start <= last_date,
        models.Event.is_active == True
    ).all()
    
    for event_obj in event_objects:
        location = db.query(models.Location).filter(
            models.Location.id == event_obj.location_id
        ).first() if event_obj.location_id else None
        
        event_type_obj = db.query(models.EventType).filter(
            models.EventType.id == event_obj.event_type_id
        ).first()
        
        events.append({
            "id": event_obj.id,
            "calendar_type": "event",
            "class_id": None,
            "event_id": event_obj.id,
            "class_name": event_obj.title,
            "description": event_obj.description,
            "date": str(event_obj.event_start.date()) if event_obj.event_start else None,
            "day": None,
            "start_time": str(event_obj.event_start.time()) if event_obj.event_start else None,
            "end_time": str(event_obj.event_end.time()) if event_obj.event_end else None,
            "location_name": location.title if location else None,
            "location_id": event_obj.location_id,
            "is_dojang": location.is_dojang if location else None,
            "instructor_id": None,
            "event_type": event_type_obj.title if event_type_obj else None,
            "day_number": None,
        })
    
    # Sort by date and time
    events.sort(key=lambda x: (x["date"], x["start_time"] or ""))
    
    return events


# Get cancelled classes
@router.get("/cancelled-classes")
def get_cancelled_classes(db: Session = Depends(get_db)):
    """
    Get all upcoming cancelled classes.
    No authentication required - public information.
    """
    today = date.today()
    
    cancelled = db.query(models.ClassException).filter(
        models.ClassException.cancelled == True,
        models.ClassException.date >= today
    ).order_by(models.ClassException.date).all()
    
    # Join with class information
    result = []
    for exception in cancelled:
        if exception.class_id:
            class_info = db.query(models.Class).filter(
                models.Class.id == exception.class_id
            ).first()
            
            if class_info:
                result.append({
                    "id": exception.id,
                    "date": str(exception.date),
                    "cancelled": exception.cancelled,
                    "note": exception.note,
                    "class_id": class_info.id,
                    "class_title": class_info.title,
                    "class_description": class_info.description,
                    "start_time": str(class_info.start_time) if class_info.start_time else None,
                    "end_time": str(class_info.end_time) if class_info.end_time else None,
                })
    
    return result