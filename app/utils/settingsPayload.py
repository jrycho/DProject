from __future__ import annotations
from pydantic import BaseModel, Field, model_validator

""" 
Form shape expected from frontend
"""
class SettingsPayload(BaseModel):
    optimized_properties: list[str] = Field(..., min_length=1)
    target_goal: list[float] = Field(..., min_length=1)
    excess_weights: list[float] = Field(..., min_length=1)
    slack_weights: list[float] = Field(..., min_length=1)

    #check for same lengths
    @model_validator(mode="after")
    def check_lengths(self):
        n = len(self.target_goal)
        for name in ("excess_weights", "slack_weights"):
            if len(getattr(self, name)) != n:
                raise ValueError(f"{name} must have length {n}")
        return self