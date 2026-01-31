# api/v1/contact.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.api.v1.auth import get_current_user, get_user_role, require_roles
from app.exceptions import NotFoundError, ForbiddenError
from typing import List
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[schemas.ContactOut])
async def get_my_contacts(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all contacts for the currently logged-in user.
    Any authenticated user can access their own contacts.
    """
    user_id = UUID(current_user["id"])
    return crud.get_contacts_by_user(db, user_id)


@router.get("/{contact_id}", response_model=schemas.ContactOut)
async def get_contact(
    contact_id: int,
    current_user: dict = Depends(get_current_user),
    user_role: str = Depends(get_user_role),
    db: Session = Depends(get_db)
):
    """
    Get a specific contact by ID.
    Users can only access their own contacts.
    Admins can access any contact.
    """
    user_id = UUID(current_user["id"])

    if user_role in ["admin", "service"]:
        contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    else:
        contact = crud.get_contact(db, contact_id, user_id)

    if not contact:
        raise NotFoundError("Contact", contact_id)

    return contact


@router.post("/", response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: schemas.ContactCreate,
    current_user: dict = Depends(get_current_user),
    user_role: str = Depends(get_user_role),
    db: Session = Depends(get_db)
):
    """
    Create a new contact.
    - Regular users can only create contacts for themselves
    - Admins can create contacts for any user
    """
    user_id = UUID(current_user["id"])

    if user_role not in ["admin", "service"] and contact.user_id != user_id:
        raise ForbiddenError("You can only create contacts for yourself")

    return crud.create_contact(db, contact)


@router.put("/{contact_id}", response_model=schemas.ContactOut)
async def update_contact(
    contact_id: int,
    contact_update: schemas.ContactUpdate,
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

    if user_role in ["admin", "service"]:
        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if not db_contact:
            raise NotFoundError("Contact", contact_id)

        update_data = contact_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contact, field, value)

        db.commit()
        db.refresh(db_contact)
        return db_contact
    else:
        if contact_update.user_id is not None and contact_update.user_id != user_id:
            raise ForbiddenError("You cannot reassign contacts to other users")

        updated_contact = crud.update_contact(db, contact_id, user_id, contact_update)

        if not updated_contact:
            raise NotFoundError("Contact", contact_id)

        return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int,
    current_user: dict = Depends(get_current_user),
    user_role: str = Depends(get_user_role),
    db: Session = Depends(get_db)
):
    """
    Delete a contact.
    - Regular users can only delete their own contacts
    - Admins can delete any contact
    """
    user_id = UUID(current_user["id"])

    if user_role in ["admin", "service"]:
        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if not db_contact:
            raise NotFoundError("Contact", contact_id)
        db.delete(db_contact)
        db.commit()
    else:
        success = crud.delete_contact(db, contact_id, user_id)
        if not success:
            raise NotFoundError("Contact", contact_id)

    return None


@router.get("/user/{target_user_id}", response_model=List[schemas.ContactOut])
async def get_contacts_for_user(
    target_user_id: UUID,
    db: Session = Depends(get_db),
    user_role: str = Depends(require_roles("admin", "service"))
):
    """
    Get all contacts for a specific user.
    Only accessible by admins.
    """
    return crud.get_contacts_by_user(db, target_user_id)
