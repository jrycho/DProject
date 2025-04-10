import numpy as np
from mealpy import FloatVar, WOA
from optimizers.swarm_utils import  BaseOptimizer


""" TODO: Needs further commenting, error handling, testing """
class woa_optimizer(BaseOptimizer):

    def solve(self):
            
        if self.A_matrix is None: #called if Not calculated before
            self.A_matrix = self.properties_matrix_creator_for_genA() #changes should automatically call properties_matrix_creator_for_genA in BaseOptimizer
        else:
            pass

        lower_bounds, upper_bounds = self.bounds_creator()

        problem_dict = {
        "obj_func": lambda sol: self.swarm_fitness_function_for_genA(sol),  # Pass target
        "bounds": FloatVar(lb=lower_bounds, ub=upper_bounds, name="delta"),
        "minmax": "min",  # Minimize the difference
        "verbose": False,
        "log_to": None,
        }

        model = WOA.HI_WOA(epoch=1000, pop_size=700, verbose=False) #creates model with default parameters
        self.solution = model.solve(problem_dict) #solve problem
        self.update_flag = False #indicates calculated solution for printing
            


