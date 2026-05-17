"""WebSocket handler — Observer pattern.

Connects to robot telemetry WS and relays updates to all subscribed frontend clients.
"""

import asyncio
import json
import logging
import os
from typing import Set

from fastapi import WebSocket, WebSocketDisconnect
import websockets

logger = logging.getLogger(__name__)

ROBOT_WS_URL = os.getenv("ROBOT_WS_URL", "ws://robot:5000/ws/telemetry")

# Observer: set of currently connected frontend clients
_subscribers: Set[WebSocket] = set()


async def subscribe(websocket: WebSocket):
    """Add a frontend client to the observer list and keep the connection alive."""
    await websocket.accept()
    _subscribers.add(websocket)
    logger.info("Client subscribed — %d active", len(_subscribers))
    try:
        while True:
            # Keep connection alive; handle client-sent messages if any
            data = await websocket.receive_text()
            logger.debug("Received from client: %s", data)
    except WebSocketDisconnect:
        _subscribers.discard(websocket)
        logger.info("Client unsubscribed — %d active", len(_subscribers))


async def _broadcast(message: str):
    """Notify all observers with the latest telemetry data."""
    dead: Set[WebSocket] = set()
    for ws in _subscribers:
        try:
            await ws.send_text(message)
        except Exception:
            dead.add(ws)
    _subscribers.difference_update(dead)


async def relay_telemetry():
    """Background task: connect to robot WS and broadcast to all subscribers."""
    while True:
        try:
            async with websockets.connect(ROBOT_WS_URL) as robot_ws:
                logger.info("Connected to robot telemetry WS")
                async for message in robot_ws:
                    await _broadcast(message)
        except Exception as exc:
            logger.warning("Robot WS connection lost (%s) — reconnecting in 3s", exc)
            # Broadcast signal-lost to all clients
            await _broadcast(json.dumps({"type": "signal_lost"}))
            await asyncio.sleep(3)
