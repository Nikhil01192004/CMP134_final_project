from fastapi import FastAPI
from app.robot_client import RobotClient

app = FastAPI()

# Temporary URL (until Docker)
robot = RobotClient(base_url="http://localhost:5000")

@app.get("/")
def root():
    return {"message": "Robot Management System Running"}

@app.get("/robot/status")
def get_robot_status():
    return robot.get_status()

@app.post("/robot/move/{direction}")
def move_robot(direction: str):
    return robot.move_robot(direction)

@app.get("/robot/connection")
def connection_status():
    return {"connected": robot.is_connected()}
