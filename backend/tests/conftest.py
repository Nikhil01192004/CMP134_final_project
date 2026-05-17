"""Shared test fixtures."""

import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from main import app

# Use SQLite in-memory for tests
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def mock_robot_client():
    """Mock the robot client to avoid actual API calls during tests."""
    with patch("app.robot.client.get_robot_client") as mock:
        mock_instance = AsyncMock()
        mock_instance.get_status = AsyncMock(return_value=AsyncMock(json=lambda: {"battery": 75, "status": "idle"}))
        mock_instance.get_map = AsyncMock(return_value=AsyncMock(json=lambda: {"robot_position": {"x": 0, "y": 0}, "obstacles": []}))
        mock_instance.get_sensor = AsyncMock(return_value=AsyncMock(json=lambda: {"sensor": "data"}))
        mock_instance.move_robot = AsyncMock(return_value=AsyncMock(json=lambda: {"success": True, "new_position": {"x": 1, "y": 1}}))
        mock.return_value = mock_instance
        yield mock


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def mock_get_engine():
        """Return in-memory SQLite engine for tests."""
        return engine
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Mock the database engine and WebSocket relay to prevent actual connections
    with patch("main.get_engine", mock_get_engine):
        with patch("app.robot.ws_handler.relay_telemetry") as mock_relay:
            # Make relay_telemetry return an AsyncMock that never completes
            mock_relay.return_value = AsyncMock()
            
            with TestClient(app) as c:
                yield c
    
    app.dependency_overrides.clear()
