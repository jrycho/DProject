from pydantic import BaseModel
from typing import List, Optional

class MealItem(BaseModel):
    id: str                 # ingredient_in_meal_id
    name: str
    kcal: float
    protein: float
    carbs: float
    fats: float
    barcode: Optional[str] = None

class MealItemsResponse(BaseModel):
    meal_id: str
    items: List[MealItem]