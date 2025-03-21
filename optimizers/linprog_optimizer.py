from scipy.optimize import linprog
import numpy as np


def linprog_optimizer(settings, input_list):
    target_goal = settings.get_target_goal()
    excess_weights = settings.get_excess_weights()
    slack_weights = settings.get_slack_weights()
    optimized_properties = settings.get_optimized_properties()
    
    #minimize deviation w_plus*d_plus + w_minus*d_minus
    n = len(optimized_properties)
    n_in = len(input_list)

    
    """  
    Minimization vector creating, in shape of [x1, x2, x3, ..., xn, [d+], [d-]
    """
    

    c = np.zeros(n_in + 2 * n)  # Zero coefficients for x
    c[n_in:(n_in + n)] = slack_weights  # Weights for d+
    c[n_in + n:] = excess_weights
    #print(c)

    """  
    Asessment of target vector, transfroming input array to matrix b_eq, used standart linprog syntax
    """
    b_eq = np.array(target_goal)
    temp_A_list = []

    """ 
    Automatically creating matrix A_eq, used standart linprog syntax, for each item in input_list, for each atribute in optimized_properties, appending atribute to row, appending row to temp_A_list
    Transposition of temp_A_list and creating matrix A_eq, expanded by n*n identity matrix and n*n negative identity matrix for deviation variables
    """
    bounds = []

    for item in input_list:
        row = []
        for atribute in optimized_properties:
            row.append(getattr(item, atribute))
        temp_A_list.append(row)

        """ BOUNDS ASSESMENT LOGIC """
        """ prolly add more coefficients than priority eg. veggie part, good protein source, oils, automatic? manual override? """
        if item.priority == 1:
            bounds.append((1, None))
        else:
            bounds.append((0.1, 2))

    bounds.extend([(0, None) for _ in range(2 * n)])
    #print(temp_A_list)
    temp_A_list = np.array(temp_A_list).T
    A_eq = np.hstack([temp_A_list, np.eye(n), -np.eye(n)])
    #print(A_eq)

    """ 
    ***Automatic bounds assesment, with emphasis on main ingredients of food, user defined max values or selection of main and side ingredients
    main to none upper bound, side to upper bound of 0,5 kg or user defined?
    test for oils and what they do, if they have any tendency to overfill the meal? (maybe not as they are clear fats, lots of cals, nothing else?)
    """



    """
    results printing, needs to go to UI too, here for testing purposes, 
    TODO: flooring it to 5g? two decimal places... or try to set it already in linprog values if possible?
    """
    results = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    print(results.x[:n_in])
    


    
    for parameter in optimized_properties:
        #print(parameter)
        val = 0
        for item in range(n_in):
            val += results.x[item] * getattr(input_list[item], parameter)
        print(f"{parameter} amount is: {val}")


    return results

