from pydantic import BaseModel
from typing import Dict

class UserGoal(BaseModel):
    user_id: int
    target_macros: Dict[str, float]