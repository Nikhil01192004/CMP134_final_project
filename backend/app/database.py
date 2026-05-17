"""PostgreSQL connection — Singleton pattern for DB engine."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@postgres:5432/robot_db",
)

_engine = None


def get_engine():
    """Singleton: return a single SQLAlchemy engine instance."""
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return _engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
