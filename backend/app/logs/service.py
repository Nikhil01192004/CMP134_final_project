"""Log service — write and read mission logs."""

from typing import List
from sqlalchemy.orm import Session
from app.logs.models import MissionLog


def write_log(db: Session, username: str, command: str, response: str) -> MissionLog:
    log = MissionLog(username=username, command=command, response=response)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_logs(db: Session, limit: int = 100) -> List[MissionLog]:
    return (
        db.query(MissionLog)
        .order_by(MissionLog.timestamp.desc())
        .limit(limit)
        .all()
    )
