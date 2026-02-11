export const CORE_NUTRIENTS = [
  { key: "energy_kcal_100g", label: "Energy (kcal)" },
  { key: "proteins_100g", label: "Protein (g)" },
  { key: "carbohydrates_100g", label: "Carbs (g)" },
  { key: "fat_100g", label: "Fat (g)" },
];

export const EXTRA_NUTRIENTS = [
  { key: "fiber_100g", label: "Fiber (g)" },
  { key: "salt_100g", label: "Salt (g)" },
  { key: "sugars_100g", label: "Sugars (g)" },
  { key: "sodium_100g", label: "Sodium (g)" },
];

export const ALL_NUTRIENTS = [
  ...CORE_NUTRIENTS,
  ...EXTRA_NUTRIENTS,
];