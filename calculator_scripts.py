from scipy.optimize import linprog
#print("scipy done")
from mealpy import FloatVar, PSO, GWO, WOA
#print("mealpy done")
import numpy as np



class Ingredient():
    def __init__(self, name:str, calories:int, carbs:int, protein:int, fats:int):
        self.name = name
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fats = fats


def weiths_normalize(target_goal,excess_weights, slack_weights):
    excess_weights = np.divide(excess_weights,target_goal)
    slack_weights = np.divide(slack_weights,target_goal)   
    return excess_weights, slack_weights

def linprog_optimizer(target_goal, excess_weights, slack_weights, input_list, optimized_properties):
    #minimize deviation w_plus*d_plus + w_minus*d_minus
    n = len(optimized_properties)
    n_in = len(input_list)

    excess_weights, slack_weights = weiths_normalize(target_goal, excess_weights, slack_weights)

    
    """  
    Minimization vector creating, in shape of [x1, x2, x3, ..., xn, [d+], [d-]
    """
    

    c = np.zeros(n_in + 2 * n)  # Zero coefficients for x
    c[n_in:(n_in + n)] = slack_weights  # Weights for d+
    c[n_in + n:] = excess_weights
    #print(c)

    """  
    Asessment of target vector, transfroming input array to matrix b_eq, used standart linprog syntax
    """
    b_eq = np.array(target_goal)
    temp_A_list = []

    """ 
    Automatically creating matrix A_eq, used standart linprog syntax, for each item in input_list, for each atribute in optimized_properties, appending atribute to row, appending row to temp_A_list
    Transposition of temp_A_list and creating matrix A_eq, expanded by n*n identity matrix and n*n negative identity matrix for deviation variables
    """
    
    for item in input_list:
        row = []
        for atribute in optimized_properties:
            row.append(getattr(item, atribute))
        temp_A_list.append(row)

    #print(temp_A_list)
    temp_A_list = np.array(temp_A_list).T
    A_eq = np.hstack([temp_A_list, np.eye(n), -np.eye(n)])
    #print(A_eq)

    """ 
    TODO:
    Automatic bounds assesment, with emphasis on main ingredients of food, user defined max values or selection of main and side ingredients
    main to none upper bound, side to upper bound of 0,5 kg or user defined?
    test for oils and what they do, if they have any tendency to overfill the meal? (maybe not as they are clear fats, lots of cals, nothing else?)
    """
    bounds = [(0, 5)] * (n_in + 2 * n)


    """
    results printing, needs to go to UI too, here for testing purposes, 
    TODO: flooring it to 5g? two decimal places... or try to set it already in linprog values if possible?
    """
    results = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    print(results.x[:n_in])
    


    
    for parameter in optimized_properties:
        #print(parameter)
        val = 0
        for item in range(n_in):
            val += results.x[item] * getattr(input_list[item], parameter)
        print(f"{parameter} amount is: {val}")


    return results


""" 
testing 
"""
input_list = [
    Ingredient("Chicken Breast", 165, 0, 31, 3),
    Ingredient("Rice", 130, 28, 2, 0),
    Ingredient("Avocado", 160, 8, 2, 15),
    Ingredient("Egg", 78, 1, 6, 5),
    Ingredient("Broccoli", 55, 11, 4, 0.5),
    Ingredient("Almonds", 164, 6, 6, 14),
    Ingredient("Greek Yogurt", 100, 7, 10, 0.5),
]

target_goal = np.array([1800, 130, 120, 40])
excess_weights = np.array([10,0,0,10]) #going over 
slack_weights = np.array([7,7,10,3])  #going under
optimized_properties = ["calories", "carbs", "protein", "fats" ]
res = linprog_optimizer(target_goal, excess_weights, slack_weights, input_list, optimized_properties).x
print(target_goal)


"notes: gives too much youghurt, need to start with dynamic bounds"