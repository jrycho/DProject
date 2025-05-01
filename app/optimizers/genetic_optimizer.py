import random
import numpy as np
from mealpy.evolutionary_based import GA
from optimizers.swarm_utils import BaseOptimizer, swarm_settings



class genetic_optimizer(BaseOptimizer):
    def __init__(self, settings, input_obj):
        super().__init__( settings, input_obj)
        self.used_optimizer = GA.BaseGA
        self.swarm_settings = swarm_settings("GA")
  

