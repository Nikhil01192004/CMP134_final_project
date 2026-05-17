"""Robot REST client — Singleton httpx client with retry + exponential backoff."""

import asyncio
import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

ROBOT_BASE_URL = os.getenv("ROBOT_BASE_URL", "http://robot:5000")
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.0  # seconds

_client: Optional[httpx.AsyncClient] = None


def get_robot_client() -> httpx.AsyncClient:
    """Singleton: return a single httpx AsyncClient for the robot API."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(base_url=ROBOT_BASE_URL, timeout=10.0)
    return _client


async def _request_with_retry(method: str, path: str, **kwargs) -> httpx.Response:
    """Make an HTTP request with exponential backoff on 503 errors."""
    client = get_robot_client()
    last_exc = None
    for attempt in range(MAX_RETRIES):
        try:
            response = await client.request(method, path, **kwargs)
            if response.status_code in (500, 503):
                raise httpx.HTTPStatusError(
                    "Service Unavailable",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            return response
        except (httpx.HTTPStatusError, httpx.ConnectError, httpx.ReadTimeout) as exc:
            last_exc = exc
            wait = BACKOFF_FACTOR * (2 ** attempt)
            logger.warning("Robot request %s %s attempt %d failed — retrying in %.1fs", method, path, attempt + 1, wait)
            await asyncio.sleep(wait)
    raise last_exc  # type: ignore[misc]


async def get_status() -> dict:
    resp = await _request_with_retry("GET", "/api/status")
    return resp.json()


async def get_map() -> dict:
    resp = await _request_with_retry("GET", "/api/map")
    return resp.json()


async def get_sensor() -> dict:
    resp = await _request_with_retry("GET", "/api/sensor")
    return resp.json()


async def move_robot(x: int, y: int) -> dict:
    resp = await _request_with_retry("POST", "/api/move", json={"x": x, "y": y})
    return resp.json()


async def get_battery() -> dict:
    resp = await _request_with_retry("GET", "/api/status")
    data = resp.json()
    return {"battery": data.get("battery", 0)}
