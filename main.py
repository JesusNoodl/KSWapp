from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .database import get_db

app = FastAPI()

@app.get("/pupils/")
def read_pupils(db: Session = Depends(get_db)):
    pupils = db.query(Pupil).all()
    return pupils
