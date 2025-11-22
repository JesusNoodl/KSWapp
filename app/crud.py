from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import uuid

days_of_week = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

def create_belt(db: Session, belt: schemas.BeltCreate) -> models.Belt:
    db_belt = models.Belt(**belt.model_dump())
    db.add(db_belt)
    db.commit()
    db.refresh(db_belt)
    return db_belt

def standard_promotion(db: Session, person_id: int, location_id:int, promotions_date: datetime | None = None):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    #If the person does not exist, return an error
    if not person:
        return "not_found"
    
    #If not a student, i.e. a parent with no belt level, return an error
    if person.belt_level_id is None:
        return "no_belt"
    
    #If the person is already at the highest belt level, return an error
    max_belt_id = db.query(models.Belt.id).order_by(models.Belt.id.desc()).first()
    if max_belt_id and person.belt_level_id >= max_belt_id[0]:
        return "max_belt"

    # Increment the belt level
    person.belt_level_id += 1
    person.modified_at = datetime.now()

    # If promotions_date is not provided, use the current date
    if promotions_date is None:
        promotions_date = datetime.now()

    # Log promotion
    promotion = models.Promotions(
        student_id=person.id,
        location_id=location_id,
        promotion_date=promotions_date,
        belt_id=person.belt_level_id,
        tabs=0  # Assuming tabs is a field in Promotions, set to 0 or a default value
    )
    db.add(promotion)

    db.commit()
    db.refresh(promotion)
    return promotion

def tab_promotion(db: Session, person_id: int, location_id:int, promotion_date: datetime | None = None):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    #If the person does not exist, return an error
    if not person:
        return "not_found"
    
    #If not a student, i.e. a parent with no belt level, return an error
    if person.belt_level_id is None:
        return "no_belt"

    # If promotions_date is not provided, use the current date
    if promotion_date is None:
        promotion_date = datetime.now()

    last_promotion = db.query(models.Promotions).filter(models.Promotions.student_id == person_id).order_by(models.Promotions.id.desc(), models.Promotions.promotion_date.desc()).first()

    if last_promotion is None:
        return "no_previous_promotion"

    # Log promotion
    promotion = models.Promotions(
        student_id=person.id,
        location_id=location_id,
        promotion_date=promotion_date,
        belt_id=person.belt_level_id,
        tabs=last_promotion.tabs + 1 
    )
    db.add(promotion)

    db.commit()
    db.refresh(promotion)
    return promotion

def set_belt(db: Session, person_id: int, belt_toset_id: int, tabs_toset: int, location_id: int, promotion_date: datetime | None = None):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    #If the person does not exist, return an error
    if not person:
        return "not_found"

    # If promotions_date is not provided, use the current date
    if promotion_date is None:
        promotion_date = datetime.now()

    # Log promotion
    promotion = models.Promotions(
        student_id=person.id,
        location_id=location_id,
        promotion_date=promotion_date,
        belt_id=belt_toset_id,
        tabs=tabs_toset
    )
    db.add(promotion)

    db.commit()
    db.refresh(promotion)
    return promotion

def remove_promotion(db: Session, promotion_id: int):
    promotion = db.query(models.Promotions).filter(models.Promotions.id == promotion_id).first()
    if not promotion:
        return "not_found"
    
    student_id = promotion.student_id

    db.delete(promotion)
    db.commit()

    # Find the most recent remaining promotion for this student
    last_promotion = (
        db.query(models.Promotions)
        .filter(models.Promotions.student_id == student_id)
        .order_by(models.Promotions.promotion_date.desc(), models.Promotions.id.desc())
        .first()
    )

    # Update the student's belt_level_id
    student = db.query(models.Person).filter(models.Person.id == student_id).first()
    if student:  # Make sure student exists
        if last_promotion:
            student.belt_level_id = last_promotion.belt_id
        else:
            student.belt_level_id = None  # or lowest belt id if you prefer

        db.commit()
        db.refresh(student)

    return promotion

def enroll_person(db: Session, person: schemas.PersonCreate) -> models.Person:
    try:
        db_person = models.Person(
            **person.model_dump(),
            role_id=2,
            belt_level_id=1,
            active=True
        )
        db.add(db_person)
        db.flush()

        promotion = models.Promotions(
            student_id=db_person.id,
            promotion_date=datetime.now(),
            belt_id=db_person.belt_level_id,
            tabs=0,
            location_id=1
        )
        db.add(promotion)

        db.commit()
        db.refresh(db_person)
        return db_person

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Enrollment failed: {str(e)}")
    
def create_class(db: Session, class_: schemas.ClassCreate) -> models.Class:
    try:
        # exclude age_categories when creating Class
        class_data = class_.model_dump(exclude={"age_categories"})
        db_class = models.Class(**class_data)
        db_class.day = days_of_week[class_.day_number]  # Map day name to number
        db.add(db_class)
        db.flush()  # get db_class.id

        # Create XREF rows for each age_category_id
        for age_category_id in class_.age_categories:
            age_category_XREF = models.AgeCategoryXREF(
                class_id=db_class.id,
                age_category_id=age_category_id
            )
            db.add(age_category_XREF)

        db.commit()
        db.refresh(db_class)
        return db_class

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Class creation failed: {str(e)}"
        )

def update_person(db: Session, person_id: int, person_update: schemas.PersonUpdate) -> models.Person:
    try:
        db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
        if not db_person:
            raise HTTPException(status_code=404, detail="Person not found")

        update_data = person_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_person, key, value)

        # Set modified date
        db_person.modified_at = datetime.now()

        db.add(db_person)
        db.commit()
        db.refresh(db_person)

        return db_person

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")

def create_location(db: Session, location: schemas.LocationCreate) -> models.Location:
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    try:
        # exclude age_categories when creating Class
        event_data = event.model_dump(exclude={"age_categories"})
        db_event = models.Event(**event_data)
        db.add(db_event)
        db.flush()  # get db_event.id

        # Create XREF rows for each age_category_id
        for age_category_id in event.age_categories:
            age_category_XREF = models.AgeCategoryXREF(
                event_id=db_event.id,
                age_category_id=age_category_id
            )
            db.add(age_category_XREF)

        db.commit()
        db.refresh(db_event)
        return db_event

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Event creation failed: {str(e)}"
        )
    
def delete_event(db: Session, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        return "not_found"
    
    db.delete(event)
    db.commit()
    return event

def delete_class(db: Session, class_id: int):
    class_ = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not class_:
        return "not_found"

    db.delete(class_)
    db.commit()
    return class_

def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()

def update_user_role(db: Session, user_id: uuid.UUID, new_role: str):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        return "not_found"
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user

def update_class(db: Session, class_id: int, class_: schemas.ClassUpdate) -> models.Class:
    try:
        db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
        if not db_class:
            raise HTTPException(status_code=404, detail="Class not found")

        update_data = class_.model_dump(exclude_unset=True, exclude={"age_categories"})
        for key, value in update_data.items():
            setattr(db_class, key, value)

        # Set modified date
        db_class.modified_at = datetime.now()
        db.add(db_class)

        # --- Handle XREF updates ---
        if class_.age_categories is not None:
            # Current XREFs in DB
            current_xrefs = db.query(models.AgeCategoryXREF).filter(models.AgeCategoryXREF.class_id == class_id).all()
            current_ids = {xref.age_category_id for xref in current_xrefs}
            new_ids = set(class_.age_categories)

            # Delete XREFs that are no longer in the new list
            for xref in current_xrefs:
                if xref.age_category_id not in new_ids:
                    db.delete(xref)

            # Add XREFs that are new
            for age_category_id in new_ids - current_ids:
                new_xref = models.AgeCategoryXREF(
                    class_id=class_id,
                    age_category_id=age_category_id
                )
                db.add(new_xref)

        db.commit()
        db.refresh(db_class)
        return db_class

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
    
def create_award(db: Session, award: schemas.AwardCreate) -> models.Award:
    """
    Create a new award.
    Automatically pulls current rank from person table if rank_at_time is not provided.
    """
    # Check if person exists
    person = db.query(models.Person).filter(models.Person.id == award.person).first()
    if not person:
        return "person_not_found"
    
    # If rank_at_time is not provided, use person's current belt level
    rank_at_time = award.rank_at_time
    if rank_at_time is None:
        if person.belt_level_id is None:
            return "no_belt"
        rank_at_time = person.belt_level_id
    
    # Check if award_type exists
    award_type = db.query(models.AwardType).filter(
        models.AwardType.id == award.award_type
    ).first()
    if not award_type:
        return "award_type_not_found"
    
    # Check if event exists (if provided)
    if award.event is not None:
        event = db.query(models.Event).filter(models.Event.id == award.event).first()
        if not event:
            return "event_not_found"
    
    # Check if tournament_category exists (if provided)
    if award.tournament_category is not None:
        category = db.query(models.TournamentCategory).filter(
            models.TournamentCategory.id == award.tournament_category
        ).first()
        if not category:
            return "category_not_found"
    
    # Create the award
    new_award = models.Award(
        award_type=award.award_type,
        person=award.person,
        rank_at_time=rank_at_time,
        event=award.event,
        date_achieved=award.date_achieved if award.date_achieved else datetime.now(),
        tournament_category=award.tournament_category
    )
    
    db.add(new_award)
    db.commit()
    db.refresh(new_award)
    
    return new_award


def update_award(db: Session, award_id: int, award_update: schemas.AwardUpdate) -> models.Award:
    """
    Update an existing award.
    Only updates fields that are provided (not None).
    """
    # Find the award
    award = db.query(models.Award).filter(models.Award.id == award_id).first()
    if not award:
        return "not_found"
    
    # Get update data (only fields that were set)
    update_data = award_update.model_dump(exclude_unset=True)
    
    # Validate references if they're being updated
    if "person" in update_data:
        person = db.query(models.Person).filter(
            models.Person.id == update_data["person"]
        ).first()
        if not person:
            return "person_not_found"
    
    if "award_type" in update_data:
        award_type = db.query(models.AwardType).filter(
            models.AwardType.id == update_data["award_type"]
        ).first()
        if not award_type:
            return "award_type_not_found"
    
    if "rank_at_time" in update_data and update_data["rank_at_time"] is not None:
        belt = db.query(models.Belt).filter(
            models.Belt.id == update_data["rank_at_time"]
        ).first()
        if not belt:
            return "belt_not_found"
    
    if "event" in update_data and update_data["event"] is not None:
        event = db.query(models.Event).filter(
            models.Event.id == update_data["event"]
        ).first()
        if not event:
            return "event_not_found"
    
    if "tournament_category" in update_data and update_data["tournament_category"] is not None:
        category = db.query(models.TournamentCategory).filter(
            models.TournamentCategory.id == update_data["tournament_category"]
        ).first()
        if not category:
            return "category_not_found"
    
    # Apply updates
    for field, value in update_data.items():
        setattr(award, field, value)
    
    db.commit()
    db.refresh(award)
    
    return award


def delete_award(db: Session, award_id: int):
    """
    Delete an award by ID.
    """
    award = db.query(models.Award).filter(models.Award.id == award_id).first()
    if not award:
        return "not_found"
    
    db.delete(award)
    db.commit()
    
    return award
