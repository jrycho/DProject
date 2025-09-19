from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema

from bson import ObjectId
from typing import Any


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
