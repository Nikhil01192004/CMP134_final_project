from fastapi import FastAPI
from app.database import engine, Base
from app.models import user

app = FastAPI(title="Robot Management System")

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Robot Management Backend Running"}