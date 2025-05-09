from app.optimizers.swarm_utils import AbstractOptimizerBase
import numpy as np
class greedy_optimizer(AbstractOptimizerBase):
    
    def __init__(self, settings, input_list):
        self.settings = settings
        self.input_list = input_list
        self.solution = None
        self.A_matrix = None

    def solve(self):
        print(self.settings.get_excess_weights())
        if self.A_matrix is None:
            self.A_matrix_creator()
        else:
            pass

        target_difference = np.array(self.settings.get_target_goal())
        greedy_return = {}

        for item in range(len(self.input_list)):

            target_difference = target_difference - 0.1 * self.A_matrix[item]
            greedy_return[self.input_list[item].get_name()] = 0.1
        
        upper_bounds, lower_bounds = self.bounds_creator()
        iter = 0

        """ TODO: end cause is not working, bound amounts. It  """
        """ Does something, stop itself, check if it is alright result, still bounds missing """
        input_list = self.input_list
        #while np.all(target_difference >= -lower_bounds) and iter <100:
        while np.all((self.settings.get_target_goal()-target_difference) <= upper_bounds) and iter <1000:
            #print(target_difference <= upper_bounds
            #print(np.all(target_difference <= -lower_bounds))
            #print(np.all((self.settings.get_target_goal()-target_difference) <= upper_bounds))
            #print(iter)
            best_item = self.bang_for_buck(input_list, target_difference)
            #print(target_difference)
            #print(best_item.get_name())               

            greedy_return[best_item.get_name()] = greedy_return[best_item.get_name()] + 0.05
            target_difference = target_difference - 0.05 * self.A_matrix[input_list.index(best_item)]
            if greedy_return[best_item.get_name()] >= 2 and best_item.priority == 0:
               input_list.remove(best_item)
            """ maybe try self.get_target_goal() - target_difference <= upper bounds"""
            iter += 1
            #print(self.settings.get_target_goal()-target_difference)
        
        self.solution = greedy_return
        return self.solution
    
    """  penalty-wise vs  soft/hard bounds, combination of adding soft bounds and finding the best feasibility inside?  """

    def print_solution(self):
        print(self.solution)
        amounts_list = []
        for item in self.input_list:
           amounts_list.append( self.solution[item.get_name()] )
        res = np.zeros_like(np.array(self.A_matrix[0]))
        for item in range(len(self.input_list)):
            res = res + amounts_list[item] * self.A_matrix[item]
        for attribute in self.settings.get_optimized_properties():
            print(f"{attribute}: {res[self.settings.get_optimized_properties().index(attribute)]}")



    def get_solution(self):
        return self.solution

    def A_matrix_actualize(self):
        self.A_matrix_creator()

    def set_input_list(self, new_input_list):
        self.input_list = new_input_list
        self.A_matrix_actualize()

    def set_settings(self, new_settings):
        self.settings = new_settings
        self.A_matrix_actualize()

    def get_settings(self):
        return self.settings

    def get_input_list(self):
        return self.input_list


    def bounds_creator(self):
        upper_bounds =  self.settings.get_target_goal()*(1+(self.settings.get_excess_weights()+0.05))
        #print((self.settings.get_excess_weights()))
        #print("upper bounds: ")
        #print(upper_bounds)
        lower_bounds =  self.settings.get_target_goal()*(1-(self.settings.get_excess_weights()+0.05))
        return upper_bounds, lower_bounds

    def A_matrix_creator(self):
        A_temp = []
        for item in self.input_list:
            row = []
            for attribute in self.settings.get_optimized_properties():
                row.append(getattr(item, attribute))
            A_temp.append(row)
        self.A_matrix = np.array(A_temp)
        

    def score_counter(self, item, input_list, target_difference):
        delta = np.array(target_difference - self.A_matrix[input_list.index(item)])
        delta_norm = np.divide(delta, (target_difference + 1e-6))
        slacks = np.where(delta_norm>0,delta_norm,0)
        excess = np.where(delta_norm<0, delta_norm, 0)
        element_wise_score = -(np.multiply(self.settings.get_excess_weights(),excess))+(np.multiply(self.settings.get_slack_weights(), slacks))
        score = np.sum(element_wise_score)
        #score = np.sum(np.multiply(self.settings.get_excess_weights(),excess))+np.sum(np.multiply(self.settings.get_slacks_weights(), slacks))
        return score

    def bang_for_buck(self,input_list, target_difference):
        score_list = []
        for item in input_list:
            score_list.append(self.score_counter(item, input_list, target_difference))
        best_indx = min(score_list)
        item_to_return = input_list[score_list.index(best_indx)]
        return item_to_return