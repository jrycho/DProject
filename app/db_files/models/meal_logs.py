from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from .ingredient_entry import IngredientEntry
from typing import List

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
    meal_id: str  # from your existing /meal endpoint
    date: datetime  # when the meal log is created
    ingredients: List[IngredientEntry] = []
    type_of_meal: Optional[str] = None  # e.g., "lunch", can be added later
    user_id: Optional[str] = None       # add when user accounts are implemented
    user_settings_id: Optional[str] = None  # planned for future

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True, #allows usage of custom Python types like ObjectID
        "json_encoders": {ObjectId: str}, #converts ObjectId to string for work with JSONs, desired in frontend
    }