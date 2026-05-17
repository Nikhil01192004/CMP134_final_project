"""Logs router — mission audit log endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.service import get_current_user
from app.auth.models import User
from app.database import get_db
from app.logs.service import get_logs

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.get("/")
def list_logs(
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = get_logs(db, limit=limit)
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "username": log.username,
            "command": log.command,
            "response": log.response,
        }
        for log in logs
    ]
