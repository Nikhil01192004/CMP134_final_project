from fastapi import FastAPI
from app.auth import router as auth_router  # import your auth router

# Create FastAPI app
app = FastAPI(title="My Auth API")

# Include the auth router so all endpoints in auth.py appear in Swagger
app.include_router(auth_router)
