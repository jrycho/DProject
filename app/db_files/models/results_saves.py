from pydantic import BaseModel, Field
from typing import Optional, List, ClassVar, Set
from app.db_files.models.ingredient import Nutrients

class optimization_weights_saves(BaseModel):
    meal_id: str
    user_id: str
    results: List[dict]

class optimization_macros_saves(BaseModel):
    meal_id: str
    user_id: str
    results: List[dict]

