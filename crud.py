from sqlalchemy.orm import Session
import models
import schemas

def create_belt(db: Session, belt: BeltCreate) -> models.Belt:
    db_belt = models.Belt(**belt.dict())
    db.add(db_belt)
    db.commit()
    db.refresh(db_belt)
    return db_belt
