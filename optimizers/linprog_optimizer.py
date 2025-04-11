from scipy.optimize import linprog
from optimizers.abstract_optimizer_base import AbstractOptimizerBase
import numpy as np

class linprog_optimizer(AbstractOptimizerBase):


    def __init__(self, settings, input_obj):
        self.settings = settings
        self.input_list = input_obj.get_input_list()
        self.is_indivisible = input_obj.get_is_indivisible()
        self.n = len(self.settings.get_optimized_properties())
        self.n_in = len(self.input_list)
        self.bounds = None
        self.A_eq = None
        self.b_eq = np.array(self.settings.get_target_goal()) #b_eq is the goal in liner proggramming
        self.c = None
        self.solution = None
        self.update_flag = False


    def solve(self):
        self.c_creator()
        self.A_matrix_creator()
        self.bounds_creator()
        
        if any(self.is_indivisible) == False:
            self.solution = linprog(self.c, A_eq=self.A_eq, b_eq=self.b_eq, bounds=self.bounds, method="highs")
            #print(self.solution.x[:self.n_in])
            self.update_flag = False
        
        elif any(self.is_indivisible) == True:
            optimal_solution = linprog(self.c, A_eq=self.A_eq, b_eq=self.b_eq, bounds=self.bounds, method="highs").x[:self.n_in]
            only_indivisible = np.where(self.is_indivisible ==0, 0, optimal_solution)
            result = np.divide(only_indivisible, self.is_indivisible, out=np.zeros_like(only_indivisible, dtype=float), where=self.is_indivisible !=0)
            
            rounded_vals = np.round(result+1e-8).astype(int) #rounding to full pieces
            rounded_weight = np.multiply(rounded_vals, self.is_indivisible)
            

            filtered_bounds = []
            for i in range(self.n_in):
                if rounded_vals[i] != 0:
                    filtered_bounds.append((rounded_weight[i],rounded_weight[i]))
                else:
                    filtered_bounds.append(self.bounds[i])
                print(filtered_bounds)


            filtered_bounds.extend([(0, None) for _ in range(2 * self.n)])
            self.solution = linprog(self.c, A_eq=self.A_eq, b_eq=self.b_eq, bounds=filtered_bounds, method="highs")
            print(self.solution.x[:self.n_in])
            self.update_flag = False

        else:
            print("Error")
        
        

        """  
        Minimization vector creating, in shape of [x1, x2, x3, ..., xn, [d+], [d-]
        When calculated with, the value to minimize is [eye vector for values], + 2*[n vector for slack/excess in nutrientes]
        """
    def c_creator(self):
        c = np.zeros(self.n_in + 2 * self.n)  # Zero coefficients for x
        c[self.n_in:(self.n_in + self.n)] = self.settings.get_slack_weights()  # Weights for d+
        c[self.n_in + self.n:] = self.settings.get_excess_weights()
        self.c = c
        #minimize deviation w_plus*d_plus + w_minus*d_minus


        """ 
        Automatically creating matrix A_eq, used standart 'linprog' syntax
        for each item in input_list:
              for each atribute in optimized_properties:
                  append atribute to row
            append row to temp_A_list

        return np form (after transposition) temp_A_list:

                item1   item2   item3   item4
        cals      100     200     150     180
        carbs      20      40      30      35
        protein    10      15      12      14 ...
                                            .
                                            .
                                            .
        should be scalable on properties                     
        expanded by n*n identity matrix and n*n negative identity matrix for deviation variables
                item1   item2   item3   item4   expanded...
        cals      100     200     150     180   0
        carbs      20      40      30      35   0
        protein    10      15      12      14   0 ...
                                            .
                                            .
                                            .
        """

    def A_matrix_creator(self):
        temp_A_list = []
        for item in self.input_list:
            row = []
            for atribute in self.settings.get_optimized_properties():
                row.append(getattr(item, atribute))
            temp_A_list.append(row)
        temp_A_list = np.array(temp_A_list).T
        self.A_eq = np.hstack([temp_A_list, np.eye(self.n), -np.eye(self.n)])



        """
        results printing, needs to go to UI too, here for testing purposes, 
        TODO: flooring it to 5g? two decimal places... or try to set it already in linprog values if possible?
        """
    def print_solution(self):
        if self.update_flag == True or self.solution is None:
            self.solve()
        else:
            pass

        for parameter in self.settings.get_optimized_properties():
            #print(parameter)
            val = 0
            for item in range(self.n_in):
                val += self.solution.x[item] * getattr(self.input_list[item], parameter)
            print(f"{parameter} amount is: {val}")



    """ TODO: when known, define what from solution to return """
    """ 
    set, get methods as found in swarm_utils/AbstractOptimizerBase some references there
    """
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



        """ prolly add more coefficients than priority eg. veggie part, good protein source, oils, automatic? manual override? """

        """ BOUNDS ASSESMENT LOGIC
        Creates bounds for each ingredient, based on the priority if whole food unlimited, otherwise limited by the max amount of 200g
        Later expanded for syntax purposes so deviations are unlimited
        TODO: undividable foods.
        """
    def bounds_creator(self):
        #print("creating")
        bounds = []
        for item in self.input_list:
            if item.priority == 1:
                bounds.append((0.1, None))
            else:
                bounds.append((0.1, 2))
    
        bounds.extend([(0, None) for _ in range(2 * self.n)])
        print(bounds)
        self.bounds = bounds