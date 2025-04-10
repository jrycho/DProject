import numpy as np
class Input_obj:
    def __init__(self):
        self.input_list = []
        self.is_indivisible = [] #will be rewritten is it a sin? should use None here?

    def __str__(self):
        return f"Input list: {self.input_list}"
    


    def add_ingredient(self, ingredient):
        if ingredient not in self.input_list:
            self.input_list.append(ingredient)
        else:
            print("Ingredient already in list")
    
    def remove_ingredient(self, ingredient_name):
        for item in self.input_list:
            if ingredient_name == item:
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
        return self.is_indivisible

    def is_indivisible_eval(self):
        new_is_indivisible = []
        for item in self.input_list:
            if item.get_piece_weight() != 0.0:
                new_is_indivisible.append(item.get_piece_weight())
            else:
                new_is_indivisible.append(0)
        self.is_indivisible = np.array(new_is_indivisible)

    def set_piece_weight_by_name(self, name, weight):
        weight = weight / 100 #convert to 100g
        for ing in self.input_list:
            if ing == name:  # thanks to __eq__, this works!
                ing.set_piece_weight(weight)
                break  # optional, if names are unique
