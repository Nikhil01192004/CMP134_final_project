import httpx
import asyncio

ROBOT_API_URL = "http://localhost:5000"


class RobotService:

    async def get_status(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ROBOT_API_URL}/status")
            return response.json()

    async def move_robot(self, direction: str):

        async with httpx.AsyncClient() as client:

            payload = {"direction": direction}

            response = await client.post(
                f"{ROBOT_API_URL}/move",
                json=payload
            )

            return response.json()