from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime


"""  
Defines settings storage model
"""
class SettingsInput(BaseModel):
    excess_weights: List[float]
    slack_weights: List[float]
    optimized_properties: List[str]
    target_goal: List[float] 

class UserSettings(BaseModel, SettingsInput):
    user_id: str
    meals: Dict[str, SettingsInput] = Field(default_factory=dict)
    updated_at: Optional[datetime] = None
