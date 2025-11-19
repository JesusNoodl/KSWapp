# api/v1/awards.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.api.v1.dependencies import get_current_user
from app.crud import get_user_by_email

router = APIRouter()

# Get awards for a student
@router.get("/student/{student_id}", response_model=list[schemas.AwardOut])
def get_awards_for_student(student_id: int, db: Session = Depends(get_db)):
    result = db.query(models.Award).filter(models.Award.person == student_id).all()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Awards not found", "student_id": student_id}
        )
    return result

# Get all awards
@router.get("/", response_model=list[schemas.AwardOut])
def get_awards(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # If service role, skip email lookup
    if current_user.get("role") == "service":
        user_role = "service"
    else:
        # regular user, fetch from db
        user = get_user_by_email(db, current_user["email"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_role = user.role

    if user_role not in ["instructor", "admin", "service"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(models.Promotions).all()