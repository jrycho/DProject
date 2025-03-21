import numpy as np
from mealpy import FloatVar, PSO
from swarm_utils import swarm_fitness_function_for_genA, properties_matrix_creator_for_genA, bounds_creator


""" TODO: Needs further commenting, error handling, testing """
def pso_optimizer(settings, input_list):
    
    #target_goal = np.array(settings.get_target_goal())
    #excess_weights = np.array(settings.get_excess_weights())
    #slack_weights = np.array(settings.get_slack_weights())
    optimized_properties = np.array(settings.get_optimized_properties())

    A_matrix = properties_matrix_creator_for_genA(settings,input_list)
    
    lower_bounds, upper_bounds = bounds_creator(input_list)


    problem_dict = {
    "obj_func": lambda sol: swarm_fitness_function_for_genA(sol, settings,A_matrix, input_list),  # Pass target
    "bounds": FloatVar(lb=lower_bounds, ub=upper_bounds, name="delta"),
    "minmax": "min",  # Minimize the difference
    "verbose": False,
    "log_to": None,
    }


    model = PSO.AIW_PSO(epoch=500, pop_size=60, verbose=False)
    best_solution = model.solve(problem_dict)
    
    
    print(best_solution.solution)
    for parameter in optimized_properties:
        #print(parameter)
        val = 0
        for item in range(len(input_list)):
            val += best_solution.solution[item] * getattr(input_list[item], parameter)
        print(f"{parameter} amount is: {val}")
    
    return best_solution.solution


