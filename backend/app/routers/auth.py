from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user, require_role
from app.models.user import User  # Make sure this points to your User model

# Initialize the router
router = APIRouter()

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "role": current_user.role
    }

@router.get("/commander-only")
def commander_endpoint(user: User = Depends(require_role("Commander"))):
    return {"message": "Commander access granted"}
