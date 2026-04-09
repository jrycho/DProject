export const CORE_NUTRIENTS = [
  { key: "energy_kcal_100g", label: "Energy (kcal)" },
  { key: "proteins_100g", label: "Protein (g)" },
  { key: "carbohydrates_100g", label: "Carbs (g)" },
  { key: "fat_100g", label: "Fat (g)" },
];

export const EXTRA_NUTRIENTS = [
  { key: "saturated_fat_100g", label: "Saturated fat (g)" },
  { key: "trans_fat_100g", label: "Trans fat (g)" },
  { key: "cholesterol_100g", label: "Cholesterol (g)" },
  { key: "sugars_100g", label: "Sugars (g)" },
  { key: "fiber_100g", label: "Fiber (g)" },
  { key: "sodium_100g", label: "Sodium (g)" },
  { key: "salt_100g", label: "Salt (g)" },
  { key: "potassium_100g", label: "Potassium (g)" },
  { key: "calcium_100g", label: "Calcium (g)" },
  { key: "iron_100g", label: "Iron (g)" },
];

export const ALL_NUTRIENTS = [
  ...CORE_NUTRIENTS,
  ...EXTRA_NUTRIENTS,
];
