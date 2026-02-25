from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt

router = APIRouter(prefix="/auth", tags=["Auth"])

# Pydantic models
class RegisterSchema(BaseModel):
    username: str
    password: str
    role: str

class LoginSchema(BaseModel):
    username: str
    password: str

# In-memory user store (for testing)
fake_db = {}

# JWT secret
SECRET_KEY = "mysecretkey"

# HTTPBearer for Swagger
bearer_scheme = HTTPBearer()

# Helpers
def create_jwt(username: str, role: str):
    payload = {"sub": username, "role": role}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"username": payload["sub"], "role": payload["role"]}
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Routes
@router.post("/register")
def register_user(data: RegisterSchema):
    if data.username in fake_db:
        raise HTTPException(status_code=400, detail="User exists")
    fake_db[data.username] = {"password": data.password, "role": data.role}
    return {"message": f"User {data.username} registered"}

@router.post("/login")
def login_user(data: LoginSchema):
    user = fake_db.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt(data.username, user["role"])
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/commander-only")
def commander_only(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "Commander":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return {"message": "Commander access granted"}