"use client";
import React from "react";
import { useState } from "react";
import { getUserIngredientsSearch } from "@/utils/userIngredientsSearch";
import IngredientButton from "./IngredientButton";
import { useDebouncedEffect } from "@/utils/useDebouncedEffect";

export default function UserIngredientSearchbarComponent({
  isActive = true,
  mealId,
  onAdded,
  addIngredientFunction,
  onSelected,
}) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]); // your "searches"

  async function handleSearch() {
    const q = query.trim();
    console.log(q);
    if (!q) {
      setResults([]);
      return;
    }
    setLoading(true);
    try {
      const results = await getUserIngredientsSearch(q);
      setResults(results);
      console.log(results);
    } finally {
      setLoading(false);
    }
  }

  useDebouncedEffect(handleSearch, [query], 300);

  return (
    <>
      <div>
        <div className="mt-6 w-full md:w-[26rem]">
          <h2 className="text-lg font-semibold mb-2 ml-4 text-white">
            Search Food:
          </h2>

          <div className="flex items-center">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSearch();
              }}
              className="flex items-center w-full gap-2"
            >
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for my ingredients..."
                className="w-[65%] p-2 ml-2 bg-gray-800 border border-green-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />

              <button
                type="button"
                onClick={handleSearch}
                className="px-4 py-2 bg-green-600 border border-green-600 text-white rounded-lg hover:bg-green-500 transition"
              >
                {loading ? "..." : "Search"}
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="mt-4 ml-2 max-h-64 overflow-y-auto custom-scrollbar">
        <ul className="space-y-2 p-2">
          {results.map((item) => (
            <li
              key={item._id}
              onClick={async () => {
                onSelected?.(item);
                console.log(item);

                try {
                  await addIngredientFunction(item, mealId);

                  setQuery("");
                  setResults([]);

                  onAdded?.();
                } catch (err) {
                  console.log(err);
                }
              }}
              className="border border-green-600 bg-gray-700 p-2 rounded-lg cursor-pointer hover:bg-gray-600 transition text-white"
            >
              <strong>{item.product_name}</strong>

              <div className="text-sm text-gray-300">
                {item.nutriments.energy_kcal_100g} kcal/100 g • Protein{" "}
                {item.nutriments.proteins_100g} g/100 g • Carbohydrates{" "}
                {item.nutriments.carbohydrates_100g} g/100 g • Fats{" "}
                {item.nutriments.fat_100g} g/100 g
              </div>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
