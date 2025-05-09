from pydantic import BaseModel
"""  
Defines model for nesting, objects with a barcode and priority
"""
class IngredientEntry(BaseModel):
    barcode: str
    priority: int