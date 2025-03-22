import numpy as np

""" TODO: Needs further commenting, error handling, testing """

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

