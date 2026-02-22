from pydantic import BaseModel, Field, EmailStr, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId
from typing import Any

from typing import List
from uuid import uuid4

from app.db_files.models.pyobject import PyObjectId


"""  
User class definition for the users collection in MongoDB.
"""
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id") #Note: always unique
    username: str
    password: str
    email: EmailStr
    is_admin: bool = False
    created_at: Optional[datetime] = Field(default=datetime.now(timezone.utc))
    share_key: str = Field(default_factory=lambda: uuid4().hex)
    reset_hash: Optional[str] = None
    reset_hash_expires: Optional[datetime] = None
    last_username_change: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "examples": {
                "username": "johndoe",
                "password": "hashedpassword",
                "email": "johndoe@example.com",
                "is_admin": False
            }
        }

"""  
Class for CRUD operation of creation, form of what user inputs
"""
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


"""  
Class for public info about a user
"""
class UserPublic(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: EmailStr
    my_share_key: str = Field(alias="share_key")
    
        
    class Config:
        populate_by_name = True