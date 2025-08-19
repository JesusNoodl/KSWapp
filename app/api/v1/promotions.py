# api/v1/promotions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from datetime import datetime
from typing import Optional

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/standard_promotions/", response_model=schemas.PromotionBase)
def standard_promotion(request: schemas.StandardPromotionRequest, db: Session = Depends(database.get_db)):
    person_id = request.person_id
    location_id = request.location_id
    promotion_date = request.promotion_date
    result = crud.standard_promotion(db, person_id, location_id, promotion_date)

    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Person not found", "person_id": person_id}
        )
    elif result == "no_belt":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Person has no belt to promote from", "person_id": person_id}
        )
    elif result == "max_belt":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Person already at maximum belt", "person_id": person_id}
        )
    return result

@router.post("/tab_promotions/", response_model=schemas.PromotionBase)
def tab_promotion(request: schemas.StandardPromotionRequest, db: Session = Depends(database.get_db)):
    person_id = request.person_id
    location_id = request.location_id
    promotion_date = request.promotion_date
    result = crud.tab_promotion(db, person_id, location_id, promotion_date)

    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Person not found", "person_id": person_id}
        )
    elif result == "no_belt":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Person has no belt to promote from", "person_id": person_id}
        )
    elif result == "no_previous_promotion":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Person has no previous promotion to tab", "person_id": person_id}
        )

    return result

@router.post("/set_belt/", response_model=schemas.PromotionBase)
def set_belt(request: schemas.SetPromotionRequest, db: Session = Depends(database.get_db)):
    person_id = request.person_id
    location_id = request.location_id
    promotion_date = request.promotion_date
    tabs_toset = request.tabs
    belt_toset_id = request.belt_id
    result = crud.set_belt(db, person_id, belt_toset_id, tabs_toset, location_id, promotion_date)

    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Person not found", "person_id": person_id}
        )

    return result

@router.delete("/delete_promotion/{promotion_id}")
def delete_promotion(promotion_id: int, db: Session = Depends(database.get_db)):
    result = crud.remove_promotion(db, promotion_id)

    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Promotion not found", "promotion_id": promotion_id}
        )

    return {"status": "success", "deleted_promotion": result}

# Get all promotions
@router.get("/", response_model=list[schemas.PromotionOut])
def get_promotions(db: Session = Depends(get_db)):
    return db.query(models.Promotions).all()

# Get promoitions for a student
@router.get("/student/{student_id}", response_model=list[schemas.PromotionOut])
def get_promotions_for_student(student_id: int, db: Session = Depends(get_db)):
    result = db.query(models.Promotions).filter(models.Promotions.student_id == student_id).all()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Promotions not found", "student_id": student_id}
        )
    return result

# Get one promotion for a student
@router.get("/student/{student_id}/promotion/{promotion_id}", response_model=schemas.PromotionOut)
def get_promotion_for_student(student_id: int, promotion_id: int, db: Session = Depends(get_db)):
    result = db.query(models.Promotions).filter(models.Promotions.student_id == student_id, models.Promotions.id == promotion_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Promotion not found", "student_id": student_id, "promotion_id": promotion_id}
        )
    return result

# Get the current rank for a student
@router.get("/current/student/{student_id}/", response_model=schemas.PromotionOut)
def get_current_promotion_for_student(student_id: int, db: Session = Depends(get_db)):
    result = db.query(models.Promotions).filter(models.Promotions.student_id == student_id).order_by(models.Promotions.promotion_date.desc(), models.Promotions.id.desc()).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No promotions found", "student_id": student_id}
        )

    belt_name = db.query(models.Belt).filter(models.Belt.id == result.belt_id).first()
    response_data = result.__dict__.copy()
    response_data["belt_name"] = belt_name.name if belt_name else None
    return response_data