# app/routers/robot.py
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/robot", tags=["Robot"])

# Robot state
robot_state = {
    "x": 0,
    "y": 0,
    "status": "idle",
    "battery": 100  # percentage
}

# Request model for direct coordinate movement
class MoveRequest(BaseModel):
    x: int
    y: int

@router.get("/status")
def get_status(current_user: User = Depends(get_current_user)):
    """
    Return the current robot status with x, y coordinates.
    """
    return {
        "position": f"{robot_state['x']},{robot_state['y']}",
        "status": robot_state["status"],
        "battery": f"{robot_state['battery']}%"
    }

@router.post("/move")
def move_robot(move: MoveRequest, current_user: User = Depends(get_current_user)):
    """
    Move the robot to the specified x and y coordinates.
    """
    robot_state["x"] = move.x
    robot_state["y"] = move.y
    robot_state["status"] = f"moved to ({move.x},{move.y})"

    # Optionally decrease battery on move
    if robot_state["battery"] > 0:
        robot_state["battery"] -= 1

    return {
        "detail": f"Robot moved to ({move.x},{move.y})",
        "state": {
            "position": f"{robot_state['x']},{robot_state['y']}",
            "status": robot_state["status"],
            "battery": f"{robot_state['battery']}%"
        }
    }