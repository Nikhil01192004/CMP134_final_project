# app/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.core.security import create_access_token
from app.core.dependencies import get_current_user, require_role
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

# Request body model for login
class LoginRequest(BaseModel):
    username: str
    password: str
    role: str  # User can specify their role on creation/login

@router.post("/login")
def login(data: LoginRequest):
    """
    Login endpoint: accepts any username/password/role and returns a JWT.
    This allows you to create your own users dynamically for testing.
    """
    # Normally, you would verify credentials against a database
    if not data.username or not data.password or not data.role:
        raise HTTPException(status_code=400, detail="Username, password, and role are required")

    # Create JWT token with username and role
    token = create_access_token({"sub": data.username, "role": data.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "role": current_user.role
    }

@router.get("/commander-only")
def commander_endpoint(user: User = Depends(require_role("Commander"))):
    return {
        "message": "Commander access granted",
        "user": user.username
    }