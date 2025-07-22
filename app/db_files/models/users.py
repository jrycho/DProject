from pydantic import BaseModel, Field, EmailStr, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from typing import Optional
from datetime import datetime
from bson import ObjectId
from typing import Any

from typing import List
from uuid import uuid4

"""  
MongoDB uses ObjectId for its _id fields, but Pydantic doesn't natively know how to handle them. PyObjectId teaches Pydantic:
- It defines a custom validator that checks if the value is a valid ObjectId.
- It updates the schema to indicate that the field should be treated as a string.

cls is the class that the validator is defined in.
v is value to be validated.
"""
class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema())

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):  
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> dict:
        json_schema = handler(schema)
        json_schema.update(type="string")
        return json_schema


"""  
User class definition for the users collection in MongoDB.
"""
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id") #Note: always unique
    username: str
    password: str
    email: EmailStr
    is_admin: bool = False
    created_at: Optional[datetime] = Field(default=datetime.now())

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


    """
    #!! DELETABLE  
    @classmethod
    def from_mongo(cls, doc: dict) -> "UserPublic":
        doc = doc.copy()
        doc["_id"] = str(doc["_id"])
        return cls(**doc)
    """   
        
    class Config:
        populate_by_name = True