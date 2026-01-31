# api/v1/promotions.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.api.v1.auth import require_roles
from app.exceptions import NotFoundError

router = APIRouter()


@router.post("/standard_promotions/", response_model=schemas.PromotionBase)
def standard_promotion(
    request: schemas.StandardPromotionRequest,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """Standard belt promotion. Requires instructor, admin, or service role."""
    return crud.standard_promotion(db, request.person_id, request.location_id, request.promotion_date)


@router.post("/tab_promotions/", response_model=schemas.PromotionBase)
def tab_promotion(
    request: schemas.StandardPromotionRequest,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """Tab promotion. Requires instructor, admin, or service role."""
    return crud.tab_promotion(db, request.person_id, request.location_id, request.promotion_date)


@router.post("/set_belt/", response_model=schemas.PromotionBase)
def set_belt(
    request: schemas.SetPromotionRequest,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """Set a specific belt for a student. Requires instructor, admin, or service role."""
    return crud.set_belt(
        db,
        request.person_id,
        request.belt_id,
        request.tabs,
        request.location_id,
        request.promotion_date
    )


@router.delete("/delete_promotion/{promotion_id}")
def delete_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """Delete a promotion. Requires instructor, admin, or service role."""
    result = crud.remove_promotion(db, promotion_id)
    return {"status": "success", "deleted_promotion": result}


@router.get("/", response_model=list[schemas.PromotionOut])
def get_promotions(
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """Get all promotions. Requires instructor, admin, or service role."""
    return db.query(models.Promotions).all()


@router.get("/student/{student_id}", response_model=list[schemas.PromotionOut])
def get_promotions_for_student(student_id: int, db: Session = Depends(get_db)):
    """Get all promotions for a student. Public endpoint."""
    result = db.query(models.Promotions).filter(models.Promotions.student_id == student_id).all()
    return result if result else []


@router.get("/student/{student_id}/promotion/{promotion_id}", response_model=schemas.PromotionOut)
def get_promotion_for_student(student_id: int, promotion_id: int, db: Session = Depends(get_db)):
    """Get a specific promotion for a student. Public endpoint."""
    result = db.query(models.Promotions).filter(
        models.Promotions.student_id == student_id,
        models.Promotions.id == promotion_id
    ).first()
    if result is None:
        raise NotFoundError("Promotion", promotion_id)
    return result


@router.get("/current/student/{student_id}/", response_model=schemas.PromotionOut)
def get_current_promotion_for_student(student_id: int, db: Session = Depends(get_db)):
    """Get the current rank for a student. Public endpoint."""
    result = db.query(models.Promotions).filter(
        models.Promotions.student_id == student_id
    ).order_by(
        models.Promotions.promotion_date.desc(),
        models.Promotions.id.desc()
    ).first()

    if result is None:
        raise NotFoundError("Promotion for student", student_id)

    belt_name = db.query(models.Belt).filter(models.Belt.id == result.belt_id).first()
    response_data = result.__dict__.copy()
    response_data["belt_name"] = belt_name.name if belt_name else None
    return response_data
