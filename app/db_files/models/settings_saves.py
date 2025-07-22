from pydantic import BaseModel
from typing import Dict, List


"""  
Defines settings storage model
"""
class SettingsInput(BaseModel):
    excess_weights: List[float]
    slack_weights: List[float]
    optimized_properties: List[str]
    target_goal: List[float]