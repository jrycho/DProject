from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import os

router = APIRouter(prefix="/Testing", tags=["Testing"])

MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "nutrition_app")

client = AsyncIOMotorClient(MONGO_URL)

@router.delete("/danger/delete-db")
async def delete_database():
    """
    🚨 Danger: Deletes the entire MongoDB database.
    Intended for development or testing only.
    """
    try:
        await client.drop_database(DB_NAME)
        return {"message": f"Database '{DB_NAME}' deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))