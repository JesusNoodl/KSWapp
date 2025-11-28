# api/v1/contact.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.api.v1.auth import get_current_user, get_user_role
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
    contacts = crud.get_contacts_by_user(db, user_id)
    return contacts

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
    
    # Admins can view any contact
    if user_role in ["admin", "service"]:
        contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    else:
        # Regular users can only view their own contacts
        contact = crud.get_contact(db, contact_id, user_id)
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
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
    
    # If not an admin, ensure they're only creating contacts for themselves
    if user_role not in ["admin", "service"] and contact.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create contacts for yourself"
        )
    
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
    
    # Admins can update any contact
    if user_role in ["admin", "service"]:
        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if not db_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        
        # Update the contact
        update_data = contact_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contact, field, value)
        
        db.commit()
        db.refresh(db_contact)
        return db_contact
    else:
        # Regular users can only update their own contacts
        if contact_update.user_id is not None and contact_update.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot reassign contacts to other users"
            )
        
        updated_contact = crud.update_contact(db, contact_id, user_id, contact_update)
        
        if not updated_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found or you don't have permission to update it"
            )
        
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
        # Admin can delete any contact
        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if not db_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        db.delete(db_contact)
        db.commit()
    else:
        # Regular user can only delete their own contacts
        success = crud.delete_contact(db, contact_id, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found or you don't have permission to delete it"
            )
    
    return None

@router.get("/user/{target_user_id}", response_model=List[schemas.ContactOut])
async def get_contacts_for_user(
    target_user_id: UUID,
    user_role: str = Depends(get_user_role),
    db: Session = Depends(get_db)
):
    """
    Get all contacts for a specific user.
    Only accessible by admins.
    """
    if user_role not in ["admin", "service"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view other users' contacts"
        )
    
    contacts = crud.get_contacts_by_user(db, target_user_id)
    return contacts