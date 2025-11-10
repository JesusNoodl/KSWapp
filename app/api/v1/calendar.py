# app/api/v1/calendar.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel
from datetime import timedelta
from sqlalchemy import extract

router = APIRouter()

# Get full_calendar entries
@router.get("/", response_model=list[schemas.FullCalendarOut])
def get_calendar(db: Session = Depends(get_db)):
    return db.query(models.t_full_calendar).all()

# Get full_calendar entries for a given month
@router.get("/year/{year}/month/{month}", response_model=list[schemas.FullCalendarOut])
def get_calendar_month(year: int, month: int, db: Session = Depends(get_db)):
    return (
        db.query(models.t_full_calendar)
        .filter(extract('year', models.t_full_calendar.c.date) == year)
        .filter(extract('month', models.t_full_calendar.c.date) == month)
        .all()
    )