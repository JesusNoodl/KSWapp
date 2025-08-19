from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine
from dotenv import load_dotenv
import os
from app.api.v1 import belts, promotions, person, class_, age_category, role, location

load_dotenv()  # Load environment variables from .env
DATABASE_URL = os.getenv("DATABASE_URL")
print("Database URL loaded:", DATABASE_URL)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(belts.router, prefix="/belts", tags=["Belts"])
app.include_router(promotions.router, prefix="/promotions", tags=["Promotions"])
app.include_router(person.router, prefix="/person", tags=["Person"])
app.include_router(class_.router, prefix="/class", tags=["Class"])
app.include_router(age_category.router, prefix="/age_category", tags=["Age Category"])
app.include_router(role.router, prefix="/role", tags=["Role"])
app.include_router(location.router, prefix="/location", tags=["Location"])

