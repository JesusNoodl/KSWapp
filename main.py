from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from .database import get_db

app = FastAPI()

@app.get("/person/")
def read_person(db: Session = Depends(get_db)):
    person = db.query(person).all()
    return person
