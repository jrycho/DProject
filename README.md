# DProject

## For right functionality install requirements.txt

use:
>  pip install -r requirements.txt

The fastAPI script is to be run by main.py file. There should not be a need to reload uvicorn.

To use the first draft that will be expanded:

### 1. Create a meal by executing
@app.post("/meal"), this will generate meal ID

### 2. To import ingredients to the meal fill
-meal ID via above
-barcode of the ingredient from OpenFoodFacts
-priority (0 for limited to 200g, 1 for unlimited amount)

### 3. Fill in @app.post("/settings") values in shape:
    {
    "optimized_properties": [
    "calories", "carbs", "protein", "fats"
    ],
    "excess_weights": [
      10,10,0,10
    ],
    "slack_weights": [
    0,4,10,0
    ],
    "target_goal": [
    1000, 100, 60, 30
    ]
    }

where 10 penalizes excessing/slacking value a lot, 0 doesnt penalize at all.
It is required to have same size of lists
other properties to use are:
        saturated_fat
        sugars
        fiber
        salt
!HOWEVER they havent been tested yet!

### 4. To get result of optimal weights for meal and settings above execute 
@app.get("/optimized_weights/{meal_id}") inputting ID of the meal.

Some barcodes:  
Chicken breast: 0023700162205  
Olive oil: 5051008878592  
Rice: 20071974  
Brocolli: 3560071019570  
feel free to use other barcodes to test the script and give feedback.


