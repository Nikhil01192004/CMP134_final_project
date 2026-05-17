"""Robot router — REST endpoints for robot interaction."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth.service import get_current_user, require_role
from app.auth.models import User
from app.database import get_db
from app.robot import client
from app.logs.service import write_log

router = APIRouter(prefix="/api/robot", tags=["robot"])


class MoveCommand(BaseModel):
    x: int = Field(..., ge=0, le=20)
    y: int = Field(..., ge=0, le=20)


@router.get("/status")
async def robot_status(current_user: User = Depends(get_current_user)):
    try:
        return await client.get_status()
    except Exception:
        raise HTTPException(status_code=503, detail="Robot unavailable — signal lost")


@router.get("/map")
async def robot_map(current_user: User = Depends(get_current_user)):
    try:
        return await client.get_map()
    except Exception:
        raise HTTPException(status_code=503, detail="Robot unavailable — signal lost")


@router.get("/sensor")
async def robot_sensor(current_user: User = Depends(get_current_user)):
    try:
        return await client.get_sensor()
    except Exception:
        raise HTTPException(status_code=503, detail="Robot unavailable — signal lost")


@router.post("/move")
async def robot_move(
    cmd: MoveCommand,
    current_user: User = Depends(require_role("commander")),
    db: Session = Depends(get_db),
):
    try:
        result = await client.move_robot(cmd.x, cmd.y)
    except Exception:
        raise HTTPException(status_code=503, detail="Robot unavailable — signal lost")

    # Log the mission command
    write_log(
        db=db,
        username=current_user.username,
        command=f"MOVE x={cmd.x} y={cmd.y}",
        response=str(result),
    )
    return result
