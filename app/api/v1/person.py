# api/v1/person.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.api.v1.auth import get_current_user, get_user_role, require_roles
from app.database import get_db
from app.exceptions import NotFoundError, ForbiddenError
from uuid import UUID

router = APIRouter()


@router.post("/enroll", response_model=schemas.PersonOut)
def enroll_student(
    person: schemas.PersonCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """Enroll a new student. Requires admin or service role."""
    return crud.enroll_person(db, person)


@router.get("/{person_id}", response_model=schemas.FullPersonOut)
def get_person(
    person_id: int,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("user", "instructor", "admin", "service"))
):
    """Get a student by ID. Any authenticated user can view."""
    person = db.query(models.t_full_person).filter(
        models.t_full_person.c.id == person_id
    ).first()

    if person is None:
        raise NotFoundError("Person", person_id)

    return person


@router.get("/", response_model=list[schemas.PersonOut])
def get_all_people(
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("instructor", "admin", "service"))
):
    """Get all students. Requires instructor, admin, or service role."""
    return db.query(models.Person).all()


@router.get("/me/persons", response_model=list[int])
def get_my_persons(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all person IDs linked to the currently authenticated user.
    Any authenticated user can access their own linked persons.

    Returns:
        List[int]: List of person IDs associated with this user
    """
    if current_user.get("role") == "service":
        raise ForbiddenError("Service role cannot access user-specific data")

    from app.crud import get_user_by_email
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise NotFoundError("User")

    user_id = current_user.get("id")

    try:
        user_persons = db.query(models.UserPerson).filter(
            models.UserPerson.user_id == user_id
        ).all()

        return [up.person_id for up in user_persons]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch person IDs: {str(e)}"
        )


@router.put("/{person_id}", response_model=schemas.ContactOut)
async def update_person(
    person_id: int,
    person_update: schemas.PersonUpdate,
    current_user: dict = Depends(get_current_user),
    user_role: str = Depends(get_user_role),
    db: Session = Depends(get_db)
):
    """
    Update a person.
    - Regular users can only update their own linked persons
    - Admins can update any person
    """
    user_id = UUID(current_user["id"])

    if user_role in ["admin", "service"]:
        db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
        if not db_person:
            raise NotFoundError("Person", person_id)

        update_data = person_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_person, field, value)

        db.commit()
        db.refresh(db_person)
        return db_person
    else:
        if person_update.id is not None and person_update.id != user_id:
            raise ForbiddenError("You cannot edit other students' information")

        updated_person = crud.update_person(db, person_id, person_update)

        if not updated_person:
            raise NotFoundError("Person", person_id)

        return updated_person
