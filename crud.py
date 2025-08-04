from sqlalchemy.orm import Session
import models
import schemas

def create_belt(db: Session, belt: schemas.BeltCreate):
    db_belt = models.Belt(**belt.model_dump())
    db.add(db_belt)
    db.commit()
    db.refresh(db_belt)
    return db_belt