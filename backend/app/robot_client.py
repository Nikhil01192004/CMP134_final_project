import httpx
from typing import Dict

class RobotClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.timeout = 5.0
        self.max_retries = 3
        self.connected = False

    def get_status(self) -> Dict:
        for attempt in range(self.max_retries):
            try:
                response = httpx.get(
                    f"{self.base_url}/status",
                    timeout=self.timeout
                )
                response.raise_for_status()
                self.connected = True
                return response.json()

            except httpx.RequestError:
                self.connected = False
                if attempt == self.max_retries - 1:
                    return {"error": "Robot unreachable"}

            except httpx.HTTPStatusError as e:
                self.connected = False
                return {"error": f"HTTP error: {e.response.status_code}"}

        return {"error": "Unknown error"}

    def move_robot(self, direction: str) -> Dict:
        for attempt in range(self.max_retries):
            try:
                response = httpx.post(
                    f"{self.base_url}/move",
                    json={"direction": direction},
                    timeout=self.timeout
                )
                response.raise_for_status()
                self.connected = True
                return response.json()

            except httpx.RequestError:
                self.connected = False
                if attempt == self.max_retries - 1:
                    return {"error": "Robot unreachable"}

            except httpx.HTTPStatusError as e:
                self.connected = False
                return {"error": f"HTTP error: {e.response.status_code}"}

        return {"error": "Unknown error"}

    def is_connected(self) -> bool:
        return self.connected
