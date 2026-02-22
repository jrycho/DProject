from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()  # Load variables from .env

MONGO_URI = os.getenv("MONGO_URI") #, "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "nutrition_app")

if MONGO_URI.startswith("mongodb://"):
    client = AsyncIOMotorClient(MONGO_URI) #if localhost skip certificates
else:
    client = AsyncIOMotorClient(MONGO_URI,
                                tlsCAFile=certifi.where(),  
                                serverSelectionTimeoutMS=5000,) #certificates for mongo hosting
db = client[MONGO_DB_NAME]

users_collection = db["users"]
meals_collection = db["meal_logs"]
ingredients_collection = db["ingredients_collection"]
user_settings = db["user_settings"]
optimized_weights_collection = db["optimized_weights_collection "]
optimized_macros_collection = db["optimized_macros_collection"] 
user_ingredients_collection = db["user_ingredients_collection"]
user_meals_collection = db["user_meals_collection"]
temp_ingredients_collection = db["temp_ingredients_collection"]

def get_db():
    return db

async def unique_share_key_init():
    await users_collection.create_index("share_key", unique=True)