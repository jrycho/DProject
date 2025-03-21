import numpy as np

def swarm_fitness_function_for_genA(sol, settings, A_matrx, input_list):
    solution = settings.get_target_goal() - np.matmul(A_matrx,sol)
    neg_sol = np.where(solution < 0, solution, 0)
    pos_sol = np.where(solution > 0, solution, 0)
    minimize_func = (-np.dot(neg_sol, settings.get_excess_weights().T ) + np.dot(pos_sol, settings.get_slack_weights().T))
    return minimize_func

def properties_matrix_creator_for_genA(settings, input_list):
    temp_A_list = []
    for item in input_list:
        row = []
        for atribute in settings.get_optimized_properties():
            row.append(getattr(item, atribute))
        temp_A_list.append(row)
    #ret_mat = np.array(temp_A_list).T
    #print(ret_mat)
    return np.array(temp_A_list).T

def bounds_creator(input_list):
    lower_bounds = []
    upper_bounds = []
    for item in input_list:
        if item.priority == 1:
            lower_bounds.append(0.1)
            upper_bounds.append(15)
        else:
            lower_bounds.append(0.1)
            upper_bounds.append(2)
    return lower_bounds, upper_bounds

import numpy as np
from mealpy import GWO, FloatVar
from swarm_utils import swarm_fitness_function_for_genA, properties_matrix_creator_for_genA, bounds_creator


""" TODO: Needs further commenting, error handling, testing """
class BaseOptimizer:


    def __init__(self, settings, input_list):
        self.settings = settings
        self.input_list = input_list
        self.solution = None
        self.A_matrix = None
        self.update_flag = False


    def solve(self):
        raise NotImplementedError("Solve must be implemented by subclasses")
        

    def print_solution(self):
        if self.solution == None or self.update_flag == True:
            self.solve()
            print("recalculated")
        else:
            pass
        print(self.solution.solution)
        for parameter in self.settings.get_optimized_properties():
                #print(parameter)
            val = 0
            for item in range(len(self.input_list)):
                val += self.solution.solution[item] * getattr(self.input_list[item], parameter)
            print(f"{parameter} amount is: {val}")


    def get_solution(self):
        return self.solution


    def set_input_list(self, new_input_list):
        self.input_list = new_input_list
        self.A_matrix_actualize()
        self.update_flag = True


    def A_matrix_actualize(self):
        self.A_matrix = properties_matrix_creator_for_genA(self.settings,self.input_list)


    def set_settings(self, new_settings):
        self.settings = new_settings
        self.A_matrix_actualize()
        self.update_flag = True


    def get_settings(self):
        return self.settings
    

    def get_input_list(self):
        return self.input_list

