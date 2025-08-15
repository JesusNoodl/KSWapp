# api/v1/belts.py
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

@router.post("/standard_promotions/", response_model=schemas.PromotionOut)
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

@router.post("/tab_promotions/", response_model=schemas.PromotionOut)
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

@router.post("/set_belt/", response_model=schemas.PromotionOut)
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