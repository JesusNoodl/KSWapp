# api/v1/awards.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, models
from app.database import get_db
from app.api.v1.dependencies import get_current_user
from app.crud import get_user_by_email

router = APIRouter()


# GET: Get awards for a student
@router.get("/student/{student_id}", response_model=list[schemas.FullAwardOut])
def get_awards_for_student(student_id: int, db: Session = Depends(get_db)):
    """
    Get all awards for a specific student.
    Any authenticated user can view awards.
    """
    result = db.query(models.t_full_award).filter(
        models.t_full_award.c.person_id == student_id
    ).all()
    # Return empty array if no awards
    return result if result else []


# GET: Get all awards (admin only)
@router.get("/", response_model=list[schemas.FullAwardOut])
def get_awards(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get all awards in the system.
    Only instructors, admins, and service roles can access this.
    """
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
    
    return db.query(models.t_full_award).all()


# GET: Get a specific award by ID
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Award with ID {award_id} not found"
        )
    
    return award


# POST: Create a new award
@router.post("/", response_model=schemas.AwardOut, status_code=status.HTTP_201_CREATED)
def create_award(
    award: schemas.AwardCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Create a new award for a student.
    Only instructors, admins, and service roles can create awards.
    """
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
    
    result = crud.create_award(db, award)
    
    if result == "person_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Person not found", "person_id": award.person}
        )
    elif result == "no_belt":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Person has no current belt level and rank_at_time was not provided"}
        )
    elif result == "award_type_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Award type not found", "award_type_id": award.award_type}
        )
    elif result == "event_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Event not found", "event_id": award.event}
        )
    elif result == "category_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Tournament category not found", "category_id": award.tournament_category}
        )
    
    return result


# PUT: Update an award
@router.put("/{award_id}", response_model=schemas.AwardOut)
def update_award(
    award_id: int,
    award_update: schemas.AwardUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Update an existing award.
    Only instructors, admins, and service roles can update awards.
    """
    # If service role, skip email lookup
    if current_user.get("role") == "service":
        user_role = "service"
    else:
        # regular user, fetch from db
        user = get_user_by_email(db, current_user["email"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_role = user.role

    if user_role not in ["admin", "service"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    result = crud.update_award(db, award_id, award_update)
    
    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Award not found", "award_id": award_id}
        )
    elif result == "person_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Person not found"}
        )
    elif result == "award_type_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Award type not found"}
        )
    elif result == "belt_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Belt not found"}
        )
    elif result == "event_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Event not found"}
        )
    elif result == "category_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Tournament category not found"}
        )
    
    return result


# DELETE: Delete an award
@router.delete("/{award_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_award(
    award_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Delete an award.
    Only admins, and service roles can delete awards.
    """
    # If service role, skip email lookup
    if current_user.get("role") == "service":
        user_role = "service"
    else:
        # regular user, fetch from db
        user = get_user_by_email(db, current_user["email"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_role = user.role

    if user_role not in ["admin", "service"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    result = crud.delete_award(db, award_id)
    
    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Award not found", "award_id": award_id}
        )
    
    return None