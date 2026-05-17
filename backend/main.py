"""FastAPI application entry point."""

import asyncio
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_engine, Base
from app.auth.router import router as auth_router
from app.auth.service import decode_token
from app.robot.router import router as robot_router
from app.logs.router import router as logs_router
from app.robot.ws_handler import subscribe, relay_telemetry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and start telemetry relay
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    task = asyncio.create_task(relay_telemetry())
    print("\n" + "=" * 44)
    print("  Frontend  ->  http://localhost:5173")
    print("  Backend   ->  http://localhost:8000/docs")
    print("  Robot     ->  http://localhost:5000/docs")
    print("  Robot WS  ->  http://localhost:5000/test")
    print("=" * 44 + "\n")
    yield
    # Shutdown
    task.cancel()


app = FastAPI(title="Robot Management System", version="1.0.0", lifespan=lifespan)

# CORS — allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST routers
app.include_router(auth_router)
app.include_router(robot_router)
app.include_router(logs_router)


# WebSocket endpoint for frontend telemetry
@app.websocket("/ws/telemetry")
async def telemetry_ws(websocket: WebSocket):
    # Extract token from query params
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Token required")
        return
    
    # Validate JWT token
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if not username:
            await websocket.close(code=1008, reason="Invalid token")
            return
    except Exception as exc:
        logger.warning("WebSocket auth failed: %s", exc)
        await websocket.close(code=1008, reason="Unauthorized")
        return
    
    # Token valid — subscribe client
    logger.info("WebSocket client authenticated: %s", username)
    await subscribe(websocket)


@app.get("/health")
def health():
    return {"status": "ok"}
