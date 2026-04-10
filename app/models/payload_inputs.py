from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel, model_validator

from app.db_files.models.ingredient import Nutrients
from app.db_files.models.ingredient_entry import IngredientEntryTemp


class StrictPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SettingsPayload(StrictPayload):
    meal_type: str = Field(..., min_length=1)
    optimized_properties: List[str] = Field(..., min_length=1)
    target_goal: List[float] = Field(..., min_length=1)
    excess_weights: List[float] = Field(..., min_length=1)
    slack_weights: List[float] = Field(..., min_length=1)

    @model_validator(mode="after")
    def check_lengths(self):
        size = len(self.target_goal)
        for name in ("optimized_properties", "excess_weights", "slack_weights"):
            if len(getattr(self, name)) != size:
                raise ValueError(f"{name} must have length {size}")
        return self


class MealTypePayload(StrictPayload):
    meal_type: str = Field(..., min_length=1)


class MealLogPayload(StrictPayload):
    meal_type: str = Field(..., min_length=1)
    date: str = Field(..., min_length=10)


class MealLogWithIdPayload(MealLogPayload):
    meal_id: str = Field(..., min_length=1)


class ResetPasswordPayload(StrictPayload):
    token: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)


class ChangeUsernamePayload(StrictPayload):
    new_username: str = Field(..., min_length=3)


class EstimateUserMacrosPayload(StrictPayload):
    sex: Literal["male", "female"]
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    age: int = Field(..., gt=0)
    goal_date: str = Field(..., min_length=10)
    activity_level: Literal[
        "sedentary",
        "lightly_active",
        "moderately_active",
        "very_active",
        "athlete",
    ]
    goal: Literal["weight_loss", "maintain", "weight_gain"]


class MacroGoalsPayload(RootModel[Dict[str, float]]):
    pass


class DatedMacroGoalsPayload(StrictPayload):
    goal_date: str = Field(..., min_length=10)
    target_macros: Dict[str, float] = Field(default_factory=dict)


class DatePayload(StrictPayload):
    date: str = Field(..., min_length=10)


class UserIngredientBasePayload(StrictPayload):
    product_name: str = Field(..., min_length=1)
    priority_user: int = Field(default=0, ge=0)
    categories_tags: List[str] = Field(default_factory=list)
    pnns_groups_1: Optional[str] = None
    pnns_groups_2: Optional[str] = None
    nova_group: Optional[int] = Field(default=None, ge=0)


class UserIngredientPayload(UserIngredientBasePayload):
    nutriments: Nutrients


class SaveTempToPermPayload(UserIngredientBasePayload):
    pass


class SharedKeyPayload(StrictPayload):
    shared_key: str = Field(..., min_length=1)


class SearchPayload(StrictPayload):
    query: str = Field(..., min_length=1)


class TempIngredientPayload(IngredientEntryTemp):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class BarcodePayload(StrictPayload):
    barcode: str = Field(..., min_length=1)


class TempIngredientAmountPayload(StrictPayload):
    barcode: str = Field(..., min_length=1)
    amount: int = Field(..., gt=0)


class MealIngredientPayload(StrictPayload):
    meal_id: str = Field(..., min_length=1)


class SetAndPieceWeightsPayload(StrictPayload):
    barcode: str = Field(..., min_length=1)
    meal_id: str = Field(..., min_length=1)
    set_amount: float = Field(..., ge=0)
    piece_weight: float = Field(..., ge=0)
    min_amount: float = Field(..., ge=0)
    max_amount: float = Field(..., ge=0)

    @model_validator(mode="after")
    def check_min_max_amounts(self):
        if self.max_amount > 0 and self.min_amount > self.max_amount:
            raise ValueError("min_amount must be less than or equal to max_amount")
        return self


class OptimizationMacrosPayload(RootModel[Dict[str, Any]]):
    pass


class OptimizationWeightsPayload(RootModel[List[Dict[str, Any]]]): 
    pass
