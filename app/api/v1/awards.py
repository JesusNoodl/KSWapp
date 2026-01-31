# api/v1/awards.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.api.v1.auth import require_roles
from app.exceptions import NotFoundError

router = APIRouter()


@router.get("/student/{student_id}", response_model=list[schemas.FullAwardOut])
def get_awards_for_student(student_id: int, db: Session = Depends(get_db)):
    """
    Get all awards for a specific student.
    Any authenticated user can view awards.
    """
    result = db.query(models.t_full_award).filter(
        models.t_full_award.c.person_id == student_id
    ).all()
    return result if result else []


@router.get("/", response_model=list[schemas.FullAwardOut])
def get_awards(
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """
    Get all awards in the system.
    Only instructors, admins, and service roles can access this.
    """
    return db.query(models.t_full_award).all()


@router.get("/{award_id}", response_model=schemas.FullAwardOut)
def get_award(award_id: int, db: Session = Depends(get_db)):
    """
    Get a specific award by ID.
    Any authenticated user can view an award.
    """
    award = db.query(models.t_full_award).filter(
        models.t_full_award.c.id == award_id
    ).first()

    if not award:
        raise NotFoundError("Award", award_id)

    return award


@router.post("/", response_model=schemas.AwardOut, status_code=status.HTTP_201_CREATED)
def create_award(
    award: schemas.AwardCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """
    Create a new award for a student.
    Only instructors, admins, and service roles can create awards.
    """
    return crud.create_award(db, award)


@router.put("/{award_id}", response_model=schemas.AwardOut)
def update_award(
    award_id: int,
    award_update: schemas.AwardUpdate,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """
    Update an existing award.
    Only admins and service roles can update awards.
    """
    return crud.update_award(db, award_id, award_update)


@router.delete("/{award_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_award(
    award_id: int,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """
    Delete an award.
    Only admins and service roles can delete awards.
    """
    crud.delete_award(db, award_id)
    return None
