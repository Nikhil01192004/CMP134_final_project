"""MissionLog SQLAlchemy model."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base


class MissionLog(Base):
    __tablename__ = "mission_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    username = Column(String(50), nullable=False, index=True)
    command = Column(String(255), nullable=False)
    response = Column(Text, nullable=True)
