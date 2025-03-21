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