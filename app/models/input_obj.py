import numpy as np
class InputObject:
    def __init__(self):
        self.input_list = []
        self.is_indivisible = np.array([]) #will be rewritten is it a sin? should use None here?
        self.user_designated_values = np.array([]) 

    def __str__(self):
        return f"Input list: {self.input_list}"
    
    """  
    add unique ingredients to the list, sets it to continous search space in is indivisible, 
    user designated value is 0 by default, can be changed by user
    """
    def add_ingredient(self, ingredient):
        if ingredient not in self.input_list:
            self.input_list.append(ingredient)
            self.is_indivisible = np.append(self.is_indivisible, 0)
            self.user_designated_values = np.append(self.user_designated_values, 0)
        else:
            print("Ingredient already in list")
    
    """  
    remove ingredient from the list, sets it to continous search space in is indivisible, 
    user designated value is 0 by 
    """

    def remove_ingredient(self, ingredient_name):
        for item in self.input_list:
            if ingredient_name == item:
                self.input_list.remove(item)
        else:
            print("Ingredient not in list")

    def remove_ingredient_by_barcode(self, barcode:str):
        for item in self.input_list:
            if item.get_barcode() == barcode:
                self.input_list.remove(item)
        else:
            print("Ingredient not in list")
                       

    def get_input_list(self):
        if self.is_indivisible == []:
            self.is_indivisible_eval()
        return self.input_list

    def set_input_list(self, new_input_list:list):
        self.input_list = new_input_list
        self.is_indivisible_eval()

    def get_is_indivisible(self):
        self.is_indivisible_eval()
        return self.is_indivisible

    def get_user_designated_values(self):
        self.user_designated_values_eval()
        return self.user_designated_values
    

    """      evals if the ingredients are indivisible, if they are, the values are set to piece weights, if not, they are set to 0 
            ??? The issue is, workage with frontend, can I create it whole in FE and then load it in as a whole or do I have to eval it
            ??? Work with ingredient as it is its attribute or is the setting just for input object?
            
    """
    def is_indivisible_eval(self):
        new_is_indivisible = []
        for item in self.input_list:
            if item.get_piece_weight() != 0.0:
                new_is_indivisible.append(item.get_piece_weight())
            else:
                new_is_indivisible.append(0)
        self.is_indivisible = np.array(new_is_indivisible)

    def user_designated_values_eval(self):
        new_user_designated_values = []
        for item in self.input_list:
            if item.get_user_designated_value() != 0.0:
                new_user_designated_values.append(item.get_user_designated_value())
            else:
                new_user_designated_values.append(0)
        self.user_designated_values = np.array(new_user_designated_values)

    def set_piece_weight_by_name(self, name, weight):
        for ingredient in self.input_list:
            if ingredient == name:  # thanks to __eq__, this works!
                ingredient.set_piece_weight(weight)
                break  # optional, if names are unique

    def set_user_designated_value_by_name(self, name, value):
        for ingredient in self.input_list:
            if ingredient == name:
                ingredient.set_user_designated_value(value)
                break 