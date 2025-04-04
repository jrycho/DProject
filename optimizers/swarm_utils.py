import numpy as np

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




"""  
BaseOptimizer - class for swarm optimizers, used in GWO, WOA, PSO
solve: uses solver on given problem, implemented in name_optimizer.py files
print solution: ensures return of previously calculated values
get solution: returns solution if previously calculated, otherwise calls solve
A_matrix_actualize: linprog uses matrix of properties, swarms use A matrix as np calculation of fitness solution (A*sol = how much of property on current sol), should be called when changes to settings
set_input_list
get_input_list - set/get method to change input list; should actualize A matrix, should set a flag for recalculation if called print_solution
set_settings
get_settings - set/get method to change settings; should actualize A matrix, should set a flag for recalculation if called print_solution
bounds_creator - creates bounds for optimization problem, should be called in solve, different for each optimizer
>>
swarn_fitness_function__for_genA - fitness func, calculate solution difference of all propperties, splits them to negative and positive vals, multiplies them by weights, returns sum of differences to find minimal solution.
"""


class BaseOptimizer(AbstractOptimizerBase):


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


    def A_matrix_actualize(self):
        self.A_matrix = self.properties_matrix_creator_for_genA()


    def set_input_list(self, new_input_list):
        self.input_list = new_input_list
        self.A_matrix_actualize()
        self.update_flag = True


    def set_settings(self, new_settings):
        self.settings = new_settings
        self.A_matrix_actualize()
        self.update_flag = True


    def get_settings(self):
        return self.settings
    

    def get_input_list(self):
        return self.input_list
    
    """ 
    For whole food item infinite upper bound for non-whole foods minimum is 10g max 200g
    TODO: user bound settings, fruit/veggies
    TODO: undividable ingredients handeling
    """
    def bounds_creator(self):
        lower_bounds = []
        upper_bounds = []
        for item in self.input_list:
            if item.priority == 1:
                lower_bounds.append(0.1)
                upper_bounds.append(15)
            else:
                lower_bounds.append(0.1)
                upper_bounds.append(2)
        return lower_bounds, upper_bounds
    

    """  
    makes list of lists of properties for each item in input list, then transposes it to get matrix of properties for each item in input list
    return:
             item1   item2   item3   item4
    cals      100     200     150     180
    carbs      20      40      30      35
    protein    10      15      12      14 ...
                                        .
                                        .
                                        .
    should be scalable on properties                          
    TODO: undividable ingredients handeling
    """
    def properties_matrix_creator_for_genA(self):
        temp_A_list = []
        for item in self.input_list:
            row = []
            for atribute in self.settings.get_optimized_properties():
                row.append(getattr(item, atribute))
            temp_A_list.append(row)
        #ret_mat = np.array(temp_A_list).T
        #print(ret_mat)
        return np.array(temp_A_list).T
    
    def swarm_fitness_function_for_genA(self, sol):
        solution = self.settings.get_target_goal() - np.matmul(self.A_matrix,sol)
        neg_sol = np.where(solution < 0, solution, 0)
        pos_sol = np.where(solution > 0, solution, 0)
        minimize_func = (-np.dot(neg_sol, self.settings.get_excess_weights().T ) + np.dot(pos_sol, self.settings.get_slack_weights().T))
        return minimize_func

