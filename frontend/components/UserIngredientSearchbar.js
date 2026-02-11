"use client";
import React from "react";
import { useState } from "react";
import { getUserIngredientsSearch } from "@/utils/userIngredientsSearch";
import IngredientButton from "./IngredientButton";
import { useDebouncedEffect } from "@/utils/useDebouncedEffect";
import { addIngredient } from "@/utils/ingredientAdd";

export default function UserIngredientSearchbarComponent({
  isActive = true,
  mealId,
  onAdded,
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
    } finally {
      setLoading(false);
    }
  }

  useDebouncedEffect(handleSearch, [query], 300);

  return (
    <>
      <div>
              <div className="mt-6 w-110">
        <h2 className="text-lg font-semibold mb-2 ml-4">Search Food:</h2>
        <div className="flex items-center">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch();
          
          }}className="flex items-center w-full gap-2"
        >
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for my ingredients..."
            className="w-full p-2 border ml-2 rounded-md shadow-md"
          />

          <button
            type="button"
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={handleSearch}
          >
            {loading ? "..." : "Search"}
          </button>
        </form></div>
      </div></div>
      <div>
        <ul className="mt-4 space-y-2">
          {results.map((item) => (
            <li
              key={item._id}
              onClick={async () => {
                if (!mealId) return;
                console.log(item);
                const code =  item.code 
                await addIngredient(code, mealId);

                setQuery("");
                setResults([]);

                onAdded?.();
              }}
              className="border p-2 rounded cursor-pointer hover:bg-gray-100 transition"
            >
              <strong>{item.product_name}</strong>
              <div className="text-sm opacity-80">
                {item.kcal} kcal • P {item.protein} • C {item.carbs} • F{" "}
                {item.fat}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
