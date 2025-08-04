from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
DATABASE_URL = os.getenv("DATABASE_URL")
print("Database URL loaded:", DATABASE_URL)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/belts/", response_model=schemas.BeltResponse)
def add_belt_rank(belt: schemas.BeltCreate, db: Session = Depends(get_db)):
    return crud.create_belt(db=db, belt=belt)
