from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

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
        db_class = models.Class(**class_.model_dump())
        db.add(db_class)
        db.flush()

        for age_category_id in class_.age_categories:
            age_category_XREF = models.AgeCategoryXREF(
                class_id=db_class.id,
                age_category_id=age_category_id
            )
            db.add(age_category_XREF)
        db.flush()  # Ensure the class is created before committing
        db.commit()
        db.refresh(db_class)
        return db_class
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Class creation failed: {str(e)}")

