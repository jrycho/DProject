from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "nutrition_app")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

users_collection = db["users"]
meals_collection = db["meal_logs"]

def get_db():
    return db