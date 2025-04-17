"""  
            nutrition_data = {
                "product_name": product.get("product_name", "Unknown"),
                "energy_kcal": nutriments.get("energy-kcal_100g"),
                "fat_100g": nutriments.get("fat_100g"),
                "saturated_fat_100g": nutriments.get("saturated-fat_100g"),
                "carbohydrates_100g": nutriments.get("carbohydrates_100g"),
                "sugars_100g": nutriments.get("sugars_100g"),
                "fiber_100g": nutriments.get("fiber_100g"),
                "proteins_100g": nutriments.get("proteins_100g"),
                "salt_100g": nutriments.get("salt_100g"),
            }

"""

class Ingredient():
    def __init__(self, data, priority):
        self.name = data.get("product_name", "Unknown")
        self.calories = data.get("energy_kcal", 0.0)
        self.carbs = data.get("carbohydrates_100g", 0.0)
        self.protein = data.get("proteins_100g", 0.0)
        self.fats = data.get("fat_100g", 0.0)
        self.saturated_fat = data.get("saturated_fat_100g", 0.0)
        self.sugars = data.get("sugars_100g", 0.0)
        self.fiber = data.get("fiber_100g", 0.0)
        self.salt = data.get("salt_100g", 0.0)

        self.priority = priority
        self.piece_weight = 0.0
        self.barcode = data.get("barcode") 

    
    def get_name(self):
        return self.name
    
    def set_piece_weight(self, piece_weight):
        self.piece_weight = piece_weight / 100
    
    def get_piece_weight(self):
        return self.piece_weight
    
    def set_priority(self, new_priority):
        self.priority = new_priority

    def get_priority(self):
        return self.priority
    
    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name.lower() == other.name.lower()
        if isinstance(other, str):
            return self.name.lower() == other.lower()
        return False
    