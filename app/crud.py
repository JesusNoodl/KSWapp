from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas

def create_belt(db: Session, belt: schemas.BeltCreate) -> models.Belt:
    db_belt = models.Belt(**belt.model_dump())
    db.add(db_belt)
    db.commit()
    db.refresh(db_belt)
    return db_belt

def standard_promotion(db: Session, person_id: int, location_id:int, promotions_date: datetime):
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
    db.refresh(person)
    return person
