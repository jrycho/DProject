import numpy as np
from mealpy import GWO, FloatVar
from swarm_utils import swarm_fitness_function_for_genA, properties_matrix_creator_for_genA, bounds_creator, BaseOptimizer


""" TODO: Needs further commenting, error handling, testing """
class gwo_optimizer(BaseOptimizer):


    def solve(self):
        
        if self.A_matrix is None:
            self.A_matrix = properties_matrix_creator_for_genA(self.settings,self.input_list)
        else:
            pass

        lower_bounds, upper_bounds = bounds_creator(self.input_list)

        problem_dict = {
        "obj_func": lambda sol: swarm_fitness_function_for_genA(sol, self.settings,self.A_matrix, self.input_list),  # Pass target
        "bounds": FloatVar(lb=lower_bounds, ub=upper_bounds, name="delta"),
        "minmax": "min",  # Minimize the difference
        "verbose": False,
        "log_to": None,
        }

        model = GWO.GWO_WOA(epoch=50, pop_size=30, verbose=False)
        self.solution = model.solve(problem_dict)
        self.update_flag = False
        

