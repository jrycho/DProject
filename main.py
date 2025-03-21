<<<<<<< HEAD

from fastapi import FastAPI
from typing import List
print("fastAPI done")
print("import test done")

app = FastAPI()

class Ingredient():
    def __init__(self, name:str, calories:int, carbs:int, protein:int, fats:int):
        self.name = name
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fats = fats


#test_list
test_list = []
selected_list = []

name_list = ["apple", "banana", "cherry", "date", "elderberry"]
dull_value = 20
for item in name_list:
    item = Ingredient(item, dull_value)
    test_list.append(item)
    dull_value *= 2


for i in test_list:
    print(i.name, i.calories)




@app.post("/add_items_by_name/")
def add_items_by_name(keyword:str):

    #TODO:will be replaced by sql structure
    selected_items = list(filter(lambda item: keyword in item.name, test_list))
    
    
    selected_list.extend(selected_items)
    return {"selected_items": selected_list}



@app.delete("/remove_items_by_name/")
def remove_items_by_name(keyword:str):
    global selected_list
    selected_list = list(filter(lambda item: keyword not in item.name, selected_list))
    return {"selected_items": selected_list}



@app.get("/")
def home():
    return {"message": "FastAPI is running!"}



@app.get("/get_test_list_calories")
def get_list_calories():
    value = 0
    for item in selected_list:
        value += item.calories
    return {"calories": value}


@app.get("/get_selected_list")
def get_selected_list():
    return {"selected_items": selected_list}
=======

from fastapi import FastAPI
from typing import List
print("fastAPI done")
print("import test done")

app = FastAPI()

class Ingredient():
    def __init__(self, name:str, calories:int):
        self.name = name
        self.calories = calories

#test_list
test_list = []
selected_list = []

name_list = ["apple", "banana", "cherry", "date", "elderberry"]
dull_value = 20
for item in name_list:
    item = Ingredient(item, dull_value)
    test_list.append(item)
    dull_value *= 2


for i in test_list:
    print(i.name, i.calories)




@app.post("/add_items_by_name/")
def add_items_by_name(keyword:str):

    #TODO:will be replaced by sql structure
    selected_items = list(filter(lambda item: keyword in item.name, test_list))
    
    
    selected_list.extend(selected_items)
    return {"selected_items": selected_list}



@app.delete("/remove_items_by_name/")
def remove_items_by_name(keyword:str):
    global selected_list
    selected_list = list(filter(lambda item: keyword not in item.name, selected_list))
    return {"selected_items": selected_list}



@app.get("/")
def home():
    return {"message": "FastAPI is running!"}



@app.get("/get_test_list_calories")
def get_list_calories():
    value = 0
    for item in selected_list:
        value += item.calories
    return {"calories": value}


@app.get("/get_selected_list")
def get_selected_list():
    return {"selected_items": selected_list}
>>>>>>> aedaca66eec89f2344bcbc54cc7aab12f51ac159
