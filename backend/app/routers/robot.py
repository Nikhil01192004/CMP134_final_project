from fastapi import APIRouter, Depends
from app.services.robot_service import RobotService
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.models import Robot

router = APIRouter(prefix="/robot", tags=["Robot"])

robot_service = RobotService()


@router.get("/status")
async def get_robot_status(
    user: User = Depends(get_current_user)
):
    return await robot_service.get_status()


@router.post("/move")
async def move_robot(
    direction: str,
    user: User = Depends(require_role("Commander"))
):
    return await robot_service.move_robot(direction)
