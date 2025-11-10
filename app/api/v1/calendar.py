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


# Get full_calendar entries
@router.get("/calendar", response_model=list[schemas.FullCalendarOut])
def get_calendar(db: Session = Depends(get_db)):
    return db.query(models.t_full_calendar).all()


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