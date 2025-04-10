""" TODO: Needs further commenting, error handling, testing """

""" AbstractOptimizerBase - template of necessarry methods for optimizers, ensures unified sets/gets
methods:
solve: uses solver on given problem
print solution: ensures return of previously calculated values
get solution: returns solution
A_matrix_actualize: linprog uses matrix of properties, swarms use A matrix as np calculation of fitness solution (A*sol = how much of property on current sol), should be called when changes to settings
set_input_list
get_input_list - set/get method to change input list; should actualize A matrix, should set a flag for recalculation if called print_solution
set_settings
get_settings - set/get method to change settings; should actualize A matrix, should set a flag for recalculation if called print_solution
bounds_creator
"""

class AbstractOptimizerBase:

    def solve(self):
        raise NotImplementedError("The method 'solve' must be implemented by subclass")

    def print_solution(self):
        raise NotImplementedError("The method 'print_solution' must be implemented by subclass")

    def get_solution(self):
        raise NotImplementedError("The method 'get_solution' must be implemented by subclass")

    def A_matrix_actualize(self):
        raise NotImplementedError("The method 'A_matrix_actualize' must be implemented by subclass")

    def set_input_list(self, new_input_list):
        raise NotImplementedError("The method 'set_input_list' must be implemented by subclass")

    def set_settings(self, new_settings):
        raise NotImplementedError("The method 'set_settings' must be implemented by subclass")

    def get_settings(self):
        raise NotImplementedError("The method 'get_settings' must be implemented by subclass")

    def get_input_list(self):
        raise NotImplementedError("The method 'get_input_list' must be implemented by subclass")

    def bounds_creator(self):
        raise NotImplementedError("The method 'bounds_creator' must be implemented by subclass")

