from scipy.optimize import linprog
from swarm_utils import AbstractOptimizerBase
import numpy as np

class linprog_optimizer(AbstractOptimizerBase):


    def __init__(self, settings, input_list):
        self.settings = settings
        self.input_list = input_list
        self.n = len(self.settings.get_optimized_properties())
        self.n_in = len(self.input_list)
        self.bounds = None
        self.A_eq = None
        self.b_eq = np.array(self.settings.get_target_goal())
        self.c = None
        self.solution = None
        self.update_flag = False


    def solve(self):
        if self.update_flag == True or self.solution is None:
            self.c_creator()
            self.A_matrix_creator()
            self.bounds_creator()
            self.solution = linprog(self.c, A_eq=self.A_eq, b_eq=self.b_eq, bounds=self.bounds, method="highs")
            print(self.solution.x[:self.n_in])
            self.update_flag = False
        else:
            pass
    
        

        """  
        Minimization vector creating, in shape of [x1, x2, x3, ..., xn, [d+], [d-]
        """
    def c_creator(self):
        c = np.zeros(self.n_in + 2 * self.n)  # Zero coefficients for x
        c[self.n_in:(self.n_in + self.n)] = self.settings.get_slack_weights()  # Weights for d+
        c[self.n_in + self.n:] = self.settings.get_excess_weights()
        self.c = c
        #minimize deviation w_plus*d_plus + w_minus*d_minus


        """ 
        Automatically creating matrix A_eq, used standart linprog syntax, for each item in input_list, for each atribute in optimized_properties, appending atribute to row, appending row to temp_A_list
        Transposition of temp_A_list and creating matrix A_eq, expanded by n*n identity matrix and n*n negative identity matrix for deviation variables
        """
        """  
        Asessment of target vector, transfroming input array to matrix b_eq, used standart linprog syntax
        """
    def A_matrix_creator(self):
        temp_A_list = []
        for item in self.input_list:
            row = []
            for atribute in self.settings.get_optimized_properties():
                row.append(getattr(item, atribute))
            temp_A_list.append(row)
        #print(temp_A_list)
        temp_A_list = np.array(temp_A_list).T
        self.A_eq = np.hstack([temp_A_list, np.eye(self.n), -np.eye(self.n)])
        #print(A_eq)


        """
        results printing, needs to go to UI too, here for testing purposes, 
        TODO: flooring it to 5g? two decimal places... or try to set it already in linprog values if possible?
        """
    def print_solution(self):   
        for parameter in self.settings.get_optimized_properties():
            #print(parameter)
            val = 0
            for item in range(self.n_in):
                val += self.solution.x[item] * getattr(self.input_list[item], parameter)
            print(f"{parameter} amount is: {val}")



    """ TODO: when known, define what from solution to return """

    def get_solution(self):
        if self.update_flag is True or self.solution is None:
            self.solve()
            self.update_flag = False
        else:
            pass
        return self.solution

    def A_matrix_actualize(self):
        self.A_matrix_creator()

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


        """ BOUNDS ASSESMENT LOGIC """
        """ prolly add more coefficients than priority eg. veggie part, good protein source, oils, automatic? manual override? """
        """ 
        ***Automatic bounds assesment, with emphasis on main ingredients of food, user defined max values or selection of main and side ingredients
         main to none upper bound, side to upper bound of 0,5 kg or user defined?
         test for oils and what they do, if they have any tendency to overfill the meal? (maybe not as they are clear fats, lots of cals, nothing else?)
         """
    def bounds_creator(self):
        #print("creating")
        bounds = []
        for item in self.input_list:
            if item.priority == 1:
                bounds.append((1, None))
            else:
                bounds.append((0.1, 2))
    
        bounds.extend([(0, None) for _ in range(2 * self.n)])
        #print(bounds)
        self.bounds = bounds