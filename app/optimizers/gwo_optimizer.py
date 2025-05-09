import numpy as np
from mealpy import GWO, FloatVar
from app.optimizers.swarm_utils import  BaseOptimizer, swarm_settings #, properties_matrix_creator_for_genA, bounds_creator, swarm_fitness_function_for_genA,



""" TODO: Force pieces now rounded to 0 to round to 1 """
class gwo_optimizer(BaseOptimizer):
    def __init__(self, settings, input_obj):
        super().__init__( settings, input_obj)
        self.used_optimizer = GWO.GWO_WOA
        self.swarm_settings = swarm_settings("GWO")

   






