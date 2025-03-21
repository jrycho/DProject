
from linprog_optimizer import linprog_optimizer
from gwo_optimizer import gwo_optimizer
from woa_optimizer import woa_optimizer
from pso_optimizer import pso_optimizer
from mealpy import FloatVar, PSO, GWO, WOA
import copy
#print("mealpy done")
import numpy as np



class Ingredient():
    def __init__(self, name:str, calories:int, carbs:int, protein:int, fats:int, priority:int):
        self.name = name
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fats = fats
        self.priority = priority


class Settings():
    def __init__(self, excess_weights:list, slack_weights:list, target_goal:list, optimized_properties:list):
        self.excess_weights = excess_weights
        self.slack_weights = slack_weights
        self.target_goal = target_goal
        self.optimized_properties = optimized_properties

    def get_settings(self):
        return  self.target_goal, self.excess_weights, self.slack_weights, self.optimized_properties

    #def weiths_normalize(target_goal,excess_weights, slack_weights):
     #   excess_weights = np.divide(excess_weights,target_goal)
      #  slack_weights = np.divide(slack_weights,target_goal)   
       # return excess_weights, slack_weights

    def set_excess_weights(self, new_excess_weights:list):
        self.excess_weights = new_excess_weights

    def set_slack_weights(self, new_slack_weights:list):
        self.slack_weights = new_slack_weights

    def set_target_goal(self, new_target_goal:list):
        self.target_goal = new_target_goal

    def set_optimized_properties(self, new_optimized_properties:list):
        self.optimized_properties = new_optimized_properties

    def get_excess_weights(self):
        excess_weights_normalized= np.divide(self.excess_weights,self.target_goal)
        return excess_weights_normalized

    def get_slack_weights(self):
        slack_weights_normalized = np.divide(self.slack_weights,self.target_goal)
        return slack_weights_normalized

    def get_target_goal(self):
        return self.target_goal
    
    def get_optimized_properties(self):
        return self.optimized_properties
    
    def __str__(self):
        return f"Excess weights: {self.excess_weights}, Slack weights: {self.slack_weights}, Target goal: {self.target_goal}, Optimized properties: {self.optimized_properties}"
            

""" 
testing 
"""
input_list = [
    Ingredient("Chicken Breast", 165, 0, 31, 3, 1),
    Ingredient("Rice", 130, 28, 2, 0, 1),
    Ingredient("Avocado", 160, 8, 2, 15,0),
    Ingredient("Egg", 78, 1, 6, 5,0),
    Ingredient("Broccoli", 55, 11, 4, 0.5,0),
    Ingredient("Almonds", 164, 6, 6, 14,0),
    Ingredient("Greek Yogurt", 100, 7, 10, 0.5,0),
    Ingredient("Oil", 884, 0, 0, 100, 0)]

target_goal = np.array([800, 100, 60, 30])
excess_weights = np.array([10,2,0,10]) #going over 
slack_weights = np.array([6,4,4,0])  #going under
optimized_properties = ["calories", "carbs", "protein", "fats" ]

settings1 = Settings(excess_weights, slack_weights, target_goal, optimized_properties)
settings2 = copy.deepcopy(settings1)
target_goal_2 = np.array([1000, 100, 60, 30])
settings2.set_target_goal(target_goal_2)

#res = linprog_optimizer(settings1, input_list).x
print("GWO part")
gwo_obj = gwo_optimizer(settings1, input_list)
gwo_obj.solve()
gwo_obj.print_solution()
print("solved and printer")
gwo_obj.set_settings(settings2)
gwo_obj.print_solution()
print("printed, check for recalculated")

#res = woa_optimizer(settings1, input_list)
#res = pso_optimizer(settings1, input_list)

print("WOApart")
woa_obj = woa_optimizer(settings1, input_list)
woa_obj.solve()
woa_obj.print_solution()
print("solved and printer")
woa_obj.set_settings(settings2)
woa_obj.print_solution()
print("printed, check for recalculated")

print("PSO part")
pso_obj = pso_optimizer(settings1, input_list)
pso_obj.solve()
pso_obj.print_solution()
print("solved and printer")
pso_obj.set_settings(settings2)
pso_obj.print_solution()
print("printed, check for recalculated")

""" notes: 
gives too much youghurt, need to start with dynamic bounds
Seems like dynamic bounds fixed that
"""