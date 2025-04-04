import numpy as np
from mealpy import GWO, FloatVar
from swarm_utils import  BaseOptimizer #, properties_matrix_creator_for_genA, bounds_creator, swarm_fitness_function_for_genA,


""" TODO: Needs further commenting, error handling, testing """
class gwo_optimizer(BaseOptimizer):


    def solve(self):
        
        if self.A_matrix is None: #called if Not calculated before
            self.A_matrix = self.properties_matrix_creator_for_genA() #changes shoul automatically call properties_matrix_creator_for_genA in BaseOptimizer
            self.bounds = self.bounds_creator()
        else:
            pass
        
        lower_bounds, upper_bounds = self.bounds_creator() #creates bounds

        problem_dict = {
        "obj_func": lambda sol: self.swarm_fitness_function_for_genA(sol),  # Pass target
        "bounds": FloatVar(lb=lower_bounds, ub=upper_bounds, name="delta"),
        "minmax": "min",  # Minimize the difference
        "verbose": False,
        "log_to": None,
        }

        model = GWO.GWO_WOA(epoch=50, pop_size=30, verbose=False) #creates model with default parameters
        self.solution = model.solve(problem_dict) #solve problem
        self.update_flag = False #indicates calculated solution for printing
        

