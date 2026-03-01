from pydantic import BaseModel

class RobotStatus(BaseModel):
    robot_id: str
    status: str
    battery: int

class RobotMove(BaseModel):
    robot_id: str
    direction: str
