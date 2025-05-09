import numpy as np
from mealpy import FloatVar, PSO
from app.optimizers.swarm_utils import BaseOptimizer,swarm_settings


""" TODO: Needs further commenting, error handling, testing """

    
class pso_optimizer(BaseOptimizer):
    def __init__(self, settings, input_obj):
        super().__init__(settings, input_obj)
        self.used_optimizer = PSO.AIW_PSO
        self.swarm_settings = swarm_settings("PSO")



