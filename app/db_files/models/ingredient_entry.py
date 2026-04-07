from pydantic import BaseModel, Field
"""  
Defines model for nesting, objects with a barcode and priority
"""
class IngredientEntry(BaseModel):
    barcode: str
    priority: int
    piece_weight: float = Field(default=0, ge=0) #prevent negative values, set default value to 0 (grams of one piece to hold it in pieces)
    set_amount: float = Field(default=0, ge=0) #prevent negative values, set default value to 0 (forced grams of ingredient, if 0 then free range)
    min_amount: float = Field(default=0, ge=0)
    max_amount: float = Field(default=0, ge=0)
 
class IngredientEntryTemp(BaseModel):
    barcode: str
    amount: int
