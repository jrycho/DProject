from app.db_files.models.ingredient import IngredientDoc
from typing import Optional
from pydantic import Field
import secrets
from app.db_files.models.pyobject import PyObjectId

class User_IngredientDoc(IngredientDoc):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: str
    priority_user: int
    share_key: str = Field(default_factory=lambda: secrets.token_urlsafe(8))