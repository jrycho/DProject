from app.db_files.models.ingredient import IngredientDoc

from pydantic import Field, AliasChoices
import secrets

class User_IngredientDoc(IngredientDoc):
    user_id: str
    priority_user: int
    share_key: str = Field(default_factory=lambda: secrets.token_urlsafe(8))