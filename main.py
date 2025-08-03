from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")

print("Database URL loaded:", DATABASE_URL)  # just to check it loads correctly

app = FastAPI()  # Create FastAPI app instance

@app.get("/")
async def root():
    return {"message": "Hello World"}
