from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Load the .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)  # Debugging line

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("✅ Connection successful")
except Exception as e:
    print("❌ Connection failed:", e)