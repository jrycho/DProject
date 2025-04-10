import numpy as np
from mealpy import GWO, FloatVar
from optimizers.swarm_utils import  BaseOptimizer #, properties_matrix_creator_for_genA, bounds_creator, swarm_fitness_function_for_genA,


""" TODO: Needs further commenting, error handling, testing """
""" TODO: Force pieces now rounded to 0 to roung to 1 """
class gwo_optimizer(BaseOptimizer):


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

            model = GWO.GWO_WOA(epoch=50, pop_size=30, verbose=False) #creates model with default parameters

            self.solution = model.solve(problem_dict) #solve problem
            self.update_flag = False #indicates calculated solution for printing


            """ Space with required indivisibility """
        elif any(self.is_indivisible) == True:
            """ Quicksearch to get closer to optimal solution by indivisible ingredients """
            #region
            lower_bounds, upper_bounds = self.bounds_creator(self.input_list) #creates bounds
            problem_dict = self.problem_dict_creator(lower_bounds, upper_bounds, self.A_matrix,self.settings.get_target_goal())
            model = GWO.GWO_WOA(epoch=30, pop_size=20, verbose=False) #creates model with default parameters
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
            model = GWO.GWO_WOA(epoch=50, pop_size=30, verbose=False) #creates model with default parameters
            
            #values reconstruction
            solution = model.solve(problem_dict)
            results[mask == 0] = solution.solution
            self.solution = results
            self.update_flag = False #indicates calculated solution for printing

        else:
            print("Error")





    def problem_dict_creator(self, lower_bounds, upper_bounds, A_matrix, target_goal):
        """ TODO: make problem dict method """
        problem_dict = {
        "obj_func": lambda sol: self.swarm_fitness_function_for_genA(sol, A_matrix, target_goal),  # Pass target
        "bounds": FloatVar(lb=lower_bounds, ub=upper_bounds, name="delta"),
        "minmax": "min",  # Minimize the difference
        "verbose": False,
        "log_to": None,
        }
        return problem_dict

