from typing import Dict, List

from pydantic import BaseModel, Field


class GoalHistoryEntry(BaseModel):
    dates: List[str] = Field(default_factory=list)
    target_macros: Dict[str, float]


class UserGoals(BaseModel):
    user_id: str
    goal_history: List[GoalHistoryEntry] = Field(default_factory=list)
