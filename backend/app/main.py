from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, robot
from app.models import user

app = FastAPI(title="Robot Management System")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(robot.router)


@app.get("/")
def root():
    return {"message": "Robot Management Backend Running"}