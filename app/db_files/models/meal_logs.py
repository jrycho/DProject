from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone, date as Date
from bson import ObjectId
from .ingredient_entry import IngredientEntry, IngredientEntryTemp
from typing import List
from app.db_files.models.pyobject import PyObjectId


"""  
Defines class for meal log
meal log has:
id, 
date of generation,
list of ingredients,
type of meal (lunch, dinner, etc.),
user id (optional, for future implementation),
user settings id (optional, for future implementation)
"""
class MealLogModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    meal_id: str  # from your existing /meal endpoint
    date: str  
    created_at: datetime =Field(default_factory=lambda: datetime.now(timezone.utc)),
    ingredients: List[IngredientEntry] = []
    type_of_meal: Optional[str] = None  # e.g., "lunch", can be added later
    user_id: Optional[str] = None       # add when user accounts are implemented
    user_settings_id: Optional[str] = None  # planned for future
    


    model_config = {
        "populate_by_name": True, #Use the field aliases instead of the Python variable names when converting to a dictionary
        "arbitrary_types_allowed": True, #allows usage of custom Python types like ObjectID
        "json_encoders": {ObjectId: str}, #converts ObjectId to string for work with JSONs, desired in frontend
    }

class MealLogModelTemp(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime =Field(default_factory=lambda: datetime.now(timezone.utc))
    ingredients: List[IngredientEntryTemp] = Field(default_factory=list) 
    type_of_meal: Optional[str] = None  # e.g., "lunch", can be added later
    user_id: Optional[str] = None       # add when user accounts are implemented
    


    model_config = {
        "populate_by_name": True, #Use the field aliases instead of the Python variable names when converting to a dictionary
        "arbitrary_types_allowed": True, #allows usage of custom Python types like ObjectID
        "json_encoders": {ObjectId: str}, #converts ObjectId to string for work with JSONs, desired in frontend
    }

"""In Pydantic, Field is used to configure and control how a model attribute behaves — it doesn’t store data itself. It tells Pydantic how to validate, default, serialize, and document a field."""