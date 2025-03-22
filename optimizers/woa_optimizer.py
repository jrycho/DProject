import numpy as np
from mealpy import FloatVar, WOA
from swarm_utils import  BaseOptimizer


""" TODO: Needs further commenting, error handling, testing """
class woa_optimizer(BaseOptimizer):

    def solve(self):
            
        if self.A_matrix is None:
            self.A_matrix = self.properties_matrix_creator_for_genA()
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

        model = WOA.HI_WOA(epoch=1000, pop_size=700, verbose=False)
        self.solution = model.solve(problem_dict)
        self.update_flag = False
            


