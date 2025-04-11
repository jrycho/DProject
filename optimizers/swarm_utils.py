import numpy as np
from optimizers.abstract_optimizer_base import AbstractOptimizerBase
from mealpy import FloatVar

""" TODO: Needs further commenting, error handling, testing """



"""  
BaseOptimizer - class for swarm optimizers, used in GWO, WOA, PSO
solve: uses solver on given problem, implemented in name_optimizer.py files
print solution: ensures return of previously calculated values
get solution: returns solution if previously calculated, otherwise calls solve
A_matrix_actualize: A matrix is a properties matrix used in optimizers (differently on usage), this method actualizes it by calling relevant creator, should be called upon settings and input changes
set_input_list - 
get_input_list - set/get method to change input list; should actualize A matrix, should set update_flag = True, indicating need for recalculation if called print_solution
set_settings
get_settings - set/get method to change settings; should actualize A matrix, should set update_flag = True, indicating need for recalculation if called print_solution
bounds_creator - creates bounds for optimization problem, should be called in solve, different for each optimizer
>>
swarn_fitness_function__for_genA - fitness func, calculate solution difference of all propperties, splits them to negative and positive vals, multiplies them by weights, returns sum of differences to find minimal solution.
"""


class BaseOptimizer(AbstractOptimizerBase):


    def __init__(self, settings, input_obj):
        self.settings = settings
        self.input_list = input_obj.get_input_list()
        self.is_indivisible = input_obj.get_is_indivisible()
        self.solution = None
        self.A_matrix = None
        self.update_flag = False
        self.used_optimizer = None
        self.swarm_settings = None
        

    def print_solution(self):
        if self.solution is None or self.update_flag == True:
            self.solve()
            print("recalculated")
        else:
            pass
        print(self.solution)
        for parameter in self.settings.get_optimized_properties():
                #print(parameter)
            val = 0
            for item in range(len(self.input_list)):
                val += self.solution[item] * getattr(self.input_list[item], parameter)
            print(f"{parameter} amount is: {val}")


    def get_solution(self):
        return self.solution


    def A_matrix_actualize(self):
        self.A_matrix = self.properties_matrix_creator_for_genA(self.input_list, self.settings.get_optimized_properties())


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
    def bounds_creator(self, input_list):
        lower_bounds = []
        upper_bounds = []
        for item in input_list:
            if item.priority == 1:
                lower_bounds.append(0.1)
                upper_bounds.append(15)
            else:
                lower_bounds.append(0.1)
                upper_bounds.append(2)
        return np.array(lower_bounds), np.array(upper_bounds)
    

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
    def properties_matrix_creator_for_genA(self, input_list, optimized_properties):
        temp_A_list = []
        for item in input_list:
            row = []
            for atribute in optimized_properties:
                row.append(getattr(item, atribute))
            temp_A_list.append(row)
        #ret_mat = np.array(temp_A_list).T
        #print(ret_mat)
        return np.array(temp_A_list).T
    
    def swarm_fitness_function_for_genA(self, sol, A_matrix, target_goal):
        solution = target_goal - np.matmul(A_matrix,sol)
        neg_sol = np.where(solution < 0, solution, 0)
        pos_sol = np.where(solution > 0, solution, 0)
        minimize_func = (-np.dot(neg_sol, self.settings.get_excess_weights().T ) + np.dot(pos_sol, self.settings.get_slack_weights().T))
        return minimize_func

    def problem_dict_creator(self, lower_bounds, upper_bounds, A_matrix, target_goal):
        """ Problem dict method """
        problem_dict = {
        "obj_func": lambda sol: self.swarm_fitness_function_for_genA(sol, A_matrix, target_goal),  # Pass target
        "bounds": FloatVar(lb=lower_bounds, ub=upper_bounds, name="delta"),
        "minmax": "min",  # Minimize the difference
        "verbose": False,
        "log_to": None,
        }
        return problem_dict
    
    def create_model(self, specification):
        if specification == "final_calculation":
            params = self.swarm_settings.get_params()

        elif specification == "guess_calculation":
            params = self.swarm_settings.get_guess_params()

        return self.used_optimizer(epoch=params["epoch"], pop_size=params["pop_size"], verbose=False)


    
    def solve(self):
        """ If no indicator, do a solve. If indivisibility indicator run solve, extract optimal values and round, cut from A matrix (make lambda parsable), cut from bounds, run GWO, reconstruct"""

        if self.A_matrix is None: #called if Not calculated before
            self.A_matrix = self.properties_matrix_creator_for_genA(self.input_list,self.settings.get_optimized_properties()) #changes should automatically call properties_matrix_creator_for_genA in BaseOptimizer
            #self.bounds = self.bounds_creator(self.input_list)
        else:
            pass
        
            """ Continuous space search """
        if any(self.is_indivisible) == False:
            lower_bounds, upper_bounds = self.bounds_creator(self.input_list) #creates bounds
            problem_dict = self.problem_dict_creator(lower_bounds, upper_bounds, self.A_matrix, self.settings.get_target_goal())

            model = self.create_model("final_calculation") #creates model with default parameters

            self.solution = model.solve(problem_dict) #solve problem
            self.update_flag = False #indicates calculated solution for printing


            """ Space with required indivisibility """
        elif any(self.is_indivisible) == True:
            """ Quicksearch to get closer to optimal solution by indivisible ingredients """
            #region
            lower_bounds, upper_bounds = self.bounds_creator(self.input_list) #creates bounds
            problem_dict = self.problem_dict_creator(lower_bounds, upper_bounds, self.A_matrix,self.settings.get_target_goal())
            model = self.create_model("guess_calculation") #creates model with default parameters
            optimal_solution = model.solve(problem_dict).solution #optimal guess
            print(f"optimal solution", optimal_solution)
            print("self.is_indivisible", self.is_indivisible)
            only_indivisible = np.where(self.is_indivisible ==0, 0, optimal_solution) #uf self.is_indivisible ==0; puts there 0, else puts optimal value
            print(f"only indivisible", only_indivisible)
            #endregion  first round search


            result = np.divide(only_indivisible, self.is_indivisible, out=np.zeros_like(only_indivisible, dtype=float), where=self.is_indivisible !=0) #divide optimal values by pieces
            rounded_vals = np.round(result+1e-8).astype(int) #rounding to full pieces
            #put somewhere to reconstruct results
            filtered_A = self.A_matrix[:, rounded_vals == 0] #should leave only columns where indivisible
            filtered_lower_bounds = lower_bounds[rounded_vals == 0] #should leave only columns where indivisible
            filtered_upper_bounds = upper_bounds[rounded_vals == 0] #should leave only columns where indivisible
            mask = rounded_vals.copy()
            print(mask)
            results = np.multiply(mask.astype(float), self.is_indivisible)
            new_target_goal = self.settings.get_target_goal() - np.matmul(self.A_matrix,results).T
            print(new_target_goal)
            problem_dict = self.problem_dict_creator(filtered_lower_bounds, filtered_upper_bounds, filtered_A, new_target_goal) #new dict
            model = self.create_model("final_calculation") #creates model with default parameters
            
            #values reconstruction
            solution = model.solve(problem_dict)
            results[mask == 0] = solution.solution
            self.solution = results
            self.update_flag = False #indicates calculated solution for printing

        else:
            print("Error")


class swarm_settings():
    def __init__(self, used_optimizer):
        self.used_optimizer = used_optimizer
        print(self.used_optimizer)
        
        self.GWO_epoch = 100
        self.GWO_pop_size = 50
        self.WOA_epoch = 100
        self.WOA_pop_size = 50
        self.PSO_epoch = 100
        self.PSO_pop_size = 50

        self.GWO_epoch_guess = 100
        self.GWO_pop_size_guess = 50
        self.WOA_epoch_guess = 100
        self.WOA_pop_size_guess = 50
        self.PSO_epoch_guess = 100
        self.PSO_pop_size_guess = 50

    def get_params(self):
        name = self.used_optimizer
        return {
            "epoch": getattr(self, f"{name}_epoch"),
            "pop_size": getattr(self, f"{name}_pop_size"),
        }
    
    def get_guess_params(self):
        name = self.used_optimizer
        return {
            "epoch": getattr(self, f"{name}_epoch_guess"),
            "pop_size": getattr(self, f"{name}_pop_size_guess"),
        }
