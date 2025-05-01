from optimizers.linprog_optimizer import linprog_optimizer
from optimizers.gwo_optimizer import gwo_optimizer
from optimizers.woa_optimizer import woa_optimizer
from optimizers.pso_optimizer import pso_optimizer
from optimizers.genetic_optimizer import genetic_optimizer
from optimizers.greedy_optimizer import greedy_optimizer
from mealpy import FloatVar, PSO, GWO, WOA
from models.ingredient import Ingredient
from models.settings import Settings
from models.input_obj import InputObject
import copy
import time
#print("mealpy done")
import numpy as np


""" 
testing 
"""
input_list = [
        {
            "product_name": "Chicken Breast",
            "energy_kcal": 165,
            "carbohydrates_100g": 0,
            "proteins_100g": 31,
            "fat_100g": 3,
            "saturated_fat_100g": 1,
            "sugars_100g": 0,
            "fiber_100g": 0,
            "salt_100g": 0.1,
        },
        {
            "product_name": "Rice",
            "energy_kcal": 130,
            "carbohydrates_100g": 28,
            "proteins_100g": 2,
            "fat_100g": 0,
            "saturated_fat_100g": 1,
            "sugars_100g": 0,
            "fiber_100g": 0.4,
            "salt_100g": 0.01,
        },
        {
            "product_name": "Avocado",
            "energy_kcal": 160,
            "carbohydrates_100g": 8,
            "proteins_100g": 2,
            "fat_100g": 15,
            "saturated_fat_100g": 2.1,
            "sugars_100g": 0.7,
            "fiber_100g": 6.7,
            "salt_100g": 0.01,
        },
        {
            "product_name": "Egg",
            "energy_kcal": 78,
            "carbohydrates_100g": 1,
            "proteins_100g": 6,
            "fat_100g": 5,
            "saturated_fat_100g": 1.6,
            "sugars_100g": 1.1,
            "fiber_100g": 0,
            "salt_100g": 0.12,
        },
        {
            "product_name": "Broccoli",
            "energy_kcal": 55,
            "carbohydrates_100g": 11,
            "proteins_100g": 4,
            "fat_100g": 0.5,
            "saturated_fat_100g": 0.1,
            "sugars_100g": 2.2,
            "fiber_100g": 3.3,
            "salt_100g": 0.03,
        },
        {
            "product_name": "Almonds",
            "energy_kcal": 164,
            "carbohydrates_100g": 6,
            "proteins_100g": 6,
            "fat_100g": 14,
            "saturated_fat_100g": 1.1,
            "sugars_100g": 1.2,
            "fiber_100g": 3.5,
            "salt_100g": 0.01,
        },
        {
            "product_name": "Greek Yogurt",
            "energy_kcal": 100,
            "carbohydrates_100g": 7,
            "proteins_100g": 10,
            "fat_100g": 0.5,
            "saturated_fat_100g": 0.3,
            "sugars_100g": 4,
            "fiber_100g": 0,
            "salt_100g": 0.1,
        },
        {
            "product_name": "Oil",
            "energy_kcal": 884,
            "carbohydrates_100g": 0,
            "proteins_100g": 0,
            "fat_100g": 100,
            "saturated_fat_100g": 14,
            "sugars_100g": 0,
            "fiber_100g": 0,
            "salt_100g": 0,
        },
        {
            "product_name": "Chicken Breast",
            "energy_kcal": 165,
            "carbohydrates_100g": 0,
            "proteins_100g": 31,
            "fat_100g": 3,
            "saturated_fat_100g": 1,
            "sugars_100g": 0,
            "fiber_100g": 0,
            "salt_100g": 0.1,
        },
    ]
priority_list = ["Chicken Breast", "Rice"]


ingredients = [Ingredient(data, 0) for data in input_list]
Input_Object = InputObject()
print(ingredients)
for item in ingredients:
    if item == "Chicken Breast":
        item.set_piece_weight(50)
    if item == "Greek Yogurt":
        item.set_piece_weight(130)

    if item in priority_list:
        item.set_priority(1)
        # print(item.get_name())
        # print(item.get_priority())
    
    Input_Object.add_ingredient(item)
Input_Object.set_user_designated_value_by_name("Almonds", 40)
print(Input_Object)
#Input_Object.is_indivisible_eval()
#print(Input_Object.is_indivisible)


target_goal = np.array([1200, 150, 80, 40, 10])
excess_weights = np.array([10,10,0,10, 5]) #going over 
slack_weights = np.array([0,4,10,0, 0])  #going under
optimized_properties = ["calories", "carbs", "protein", "fats", "sugars" ]

settings1 = Settings(excess_weights, slack_weights, target_goal, optimized_properties)
settings2 = copy.deepcopy(settings1)
target_goal_2 = np.array([1000, 100, 60, 30, 10])
settings2.set_target_goal(target_goal_2)



"""
print("Linprog part")
linprog_obj = linprog_optimizer(settings1, Input_Object)
linprog_obj.solve()
linprog_obj.print_solution()

print("solved and printed")
linprog_obj.set_settings(settings2)
linprog_obj.print_solution()
print("printed, check for recalculated")
"""

print("GWO part")
gwo_obj = gwo_optimizer(settings1, Input_Object)
start = time.time()
gwo_obj.solve()
end = time.time()
print(f"⏱️ Time taken: {end - start:.4f} seconds")
gwo_obj.print_solution()

print("solved and printed")
gwo_obj.set_settings(settings2)
gwo_obj.print_solution()
print("printed, check for recalculated")

#res = woa_optimizer(settings1, input_list)
#res = pso_optimizer(settings1, input_list)
"""
print("WOApart")
woa_obj = woa_optimizer(settings1, Input_Object)
woa_obj.solve()
woa_obj.print_solution()
print("solved and printer")
woa_obj.set_settings(settings2)
woa_obj.print_solution()
print("printed, check for recalculated")

print("PSO part")
pso_obj = pso_optimizer(settings1, Input_Object)
pso_obj.solve()
pso_obj.print_solution()
print("solved and printed")
pso_obj.set_settings(settings2)
pso_obj.print_solution()
print("printed, check for recalculated")
"""

""" notes: 
gives too much youghurt, need to start with dynamic bounds
Seems like dynamic bounds fixed that
"""

"""

greedy_obj = greedy_optimizer(settings1, input_list)
greedy_obj.solve()
greedy_obj.print_solution()
print("solved and printed")
greedy_obj.set_settings(settings2)
greedy_obj.print_solution()
print("printed, check for recalculated")

print("GA part")
gwo_obj = genetic_optimizer(settings1, Input_Object)
start = time.time()
gwo_obj.solve()
end = time.time()
print(f"⏱️ Time taken: {end - start:.4f} seconds")
gwo_obj.print_solution()

print("solved and printed")
gwo_obj.set_settings(settings2)
gwo_obj.print_solution()
print("printed, check for recalculated")
"""