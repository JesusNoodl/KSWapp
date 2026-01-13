# api/v1/person.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.api.v1.auth import get_current_user, get_user_role
from app.crud import get_user_by_email
from app.database import get_db
from uuid import UUID

router = APIRouter()

# Enroll a new student
@router.post("/enroll", response_model=schemas.PersonOut)
def enroll_student(person: schemas.PersonCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
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
    return crud.enroll_person(db, person)

# Get a student by ID
@router.get("/{person_id}", response_model=schemas.FullPersonOut)
def get_person(
    person_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    # Determine user role
    if current_user.get("role") == "service":
        user_role = "service"
    else:
        # Regular user, fetch from db
        user = get_user_by_email(db, current_user["email"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_role = user.role
    
    # Check permissions
    if user_role not in ["instructor", "admin", "service", "user"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Query the full_person view instead of the Person table
    person = db.query(models.t_full_person).filter(
        models.t_full_person.c.id == person_id
    ).first()
    
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    
    return person

# Get all students
@router.get("/", response_model=list[schemas.PersonOut])
def get_all_people(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
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
    # If service role, reject (service should use different endpoint)
    if current_user.get("role") == "service":
        raise HTTPException(
            status_code=403,
            detail="Service role cannot access user-specific data"
        )
    
    # Regular user - fetch from db to verify they exist
    user = get_user_by_email(db, current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found in database")
    
    # Get the Supabase user_id (the UUID from auth)
    user_id = current_user.get("id")
    
    try:
        # Query the user_person table
        user_persons = db.query(models.UserPerson).filter(
            models.UserPerson.user_id == user_id
        ).all()
        
        # Extract person_ids
        person_ids = [up.person_id for up in user_persons]
        
        return person_ids
    
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
    Update a contact.
    - Regular users can only update their own contacts
    - Admins can update any contact
    """
    user_id = UUID(current_user["id"])
    
    # Admins can update any contact
    if user_role in ["admin", "service"]:
        db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
        if not db_person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found"
            )
        
        # Update the contact
        update_data = person_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_person, field, value)

        db.commit()
        db.refresh(db_person)
        return db_person
    else:
        # Regular users can only update their own contacts
        if person_update.id is not None and person_update.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot edit other students information"
            )

        updated_person = crud.update_person(db, person_id, person_update)

        if not updated_person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found or you don't have permission to update it"
            )

        return updated_person