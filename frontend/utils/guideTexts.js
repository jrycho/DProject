// Guide texts for different pages and components
export const guideTexts = {
  mealLoggerHome: {
    title: "How to Build and Optimize a Meal",
    content: "Start by creating or selecting a meal in Meal Logger, then add ingredients to it from your ingredient database.<n>Use set amount when an ingredient must stay fixed, and enter that amount in grams.<n>Piece weights are useful for foods counted in pieces, such as biscuits, when you want to include whole pieces instead of cut or partial pieces.<n>Minimum value and maximum value define the allowed range for each ingredient during optimization.<n>Do not forget to set your meal settings before optimizing.<n>When your meal, settings, and limits are ready, press Optimize to generate the adjusted ingredient amounts."
  },
  mealLoggerSettings: {
    title: "How Settings Work",
    content: "Use these settings to tell the optimizer what you want the selected meal to aim for.<n>Target value is the amount you want for a nutrient.<n>Excess says how strongly the optimizer should avoid going above that value.<n>Slack says how acceptable it is to stay below that value if needed.<n>The optimizer will try to find the best possible result automatically.<n>If your ingredients or limits do not allow a perfect result, it will still give you the best match it can."
  },
  trackerGoals: {
    title: "How Goal Estimates Work",
    content: "The smart estimate uses a higher-protein setup of about 1.7 g per kilogram of body weight together with a Mifflin-based calorie recommendation.<n>This gives you a recommended daily baseline that can help you understand what a balanced day of eating may look like.<n>You can then split these daily targets across your meals in whatever way fits you best.<n>For example, if you prefer a smaller breakfast and a larger dinner, you can divide your daily intake that way.<n>Please note that this estimate does not include extra activity you may do during the day."
  },
  myAccountSharing: {
    title: "Sharing Keys",
    content: "Sharing keys let you share your created ingredient database with someone else.<n>Anyone who has your share key can add it and access your ingredients.<n>This works one way only, so adding someone else's key does not automatically give them access to your ingredients.<n>If you want to share with each other, both people need to exchange and add the other person's key."
  },
  addIngredients: {
    title: "Adding Ingredients via Macros",
    content: "This page allows you to create custom ingredients by manually entering their nutritional values.<n>Fill in the ingredient name, select its priority (main or supporting), and enter the macro and micronutrient values per 100g.<n>Use the '+ Add nutrients' button to include additional nutrients beyond the core ones (proteins, carbs, fats, calories).<n>All values should be entered per 100 grams of the ingredient."
  },
  addIngredientsFromDb: {
    title: "Building an Ingredient from Existing Ingredients",
    content: "This page lets you create a custom ingredient by combining ingredients that already exist in the database.<n>Use 'Find ingredients' for the shared database or 'My ingredients' for your own saved items, then add each ingredient to the temporary list.<n>Adjust the amount of each item so the temporary ingredient matches your recipe or meal as closely as possible.<n>When the list is ready, enter a name and priority, then save it to your permanent ingredient database."
  },
  addIngredientsTotalBatch: {
    title: "Adding an Ingredient from Batch Totals",
    content: "This page is for recipes where you know the total nutrients of the whole batch rather than the values per 100g.<n>Enter the ingredient name, choose its priority, and provide the final batch weight in grams.<n>Fill in the nutrient totals for the entire batch, then use '+ Add nutrients' if you want to include more than the core values.<n>The app will automatically convert the totals into values per 100 grams before saving the ingredient."
  }
};
