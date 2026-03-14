// app/ingredients/add-macros/page.jsx
"use client";

import { useState } from "react";
import { addUserIngredientDirect } from "@/utils/userIngredientDirectMacros";
import ProtectedPage from "@/components/ProtectedPage";
import Navbar from "@/components/Navbar";
import ThreadsBackground from "@/components/ThreadsBackground";
import {
  CORE_NUTRIENTS,
  EXTRA_NUTRIENTS,
} from "@/utils/userIngredientsNutrientsConfig";
import IngredientModeSwitcher from "@/components/UserIngredientSwitcher";

export default function AddMacrosSimple() {
  /* Basic */
  const [name, setName] = useState("");
  const [priorityUser, setPriorityUser] = useState("");

  // ✅ NEW: final batch weight (g)
  const [totalWeightG, setTotalWeightG] = useState("");

  /* Selected nutrients (core always included) */
  const [selected, setSelected] = useState(CORE_NUTRIENTS.map((n) => n.key));

  /* Nutrient values (TOTALS for whole batch) */
  const [values, setValues] = useState({});

  /* UI state */
  const [showExtras, setShowExtras] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function toggleExtra(key) {
    setSelected((prev) =>
      prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key],
    );
  }

  function setNutrientValue(key, val) {
    setValues((prev) => ({
      ...prev,
      [key]: val,
    }));
  }

  const ALL = [...CORE_NUTRIENTS, ...EXTRA_NUTRIENTS];

  // ✅ normalized nutriments helper (per 100g)
  function buildNutrimentsNormalized() {
    const w = Number(totalWeightG);
    const nutriments = {};

    selected.forEach((key) => {
      const total = Number(values[key] ?? 0);
      nutriments[key] = w > 0 ? (total / w) * 100 : 0;
    });

    return nutriments;
  }

  async function onSubmit(e) {
    e.preventDefault();

    setError("");
    setResult(null);
    setLoading(true);

    const payload = {
      product_name: name,
      priority_user: priorityUser,
      nutriments: buildNutrimentsNormalized(), // ✅ division happens here
      categories_tags: ["custom"],
    };

    try {
      const data = await addUserIngredientDirect(payload);
      setResult(data);

      // Reset
      setName("");
      setPriorityUser("");
      setTotalWeightG("");
      setValues({});
      setSelected(CORE_NUTRIENTS.map((n) => n.key));
    } catch (err) {
      setError(err.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }
  return (
    <ProtectedPage>
      <main className="relative min-h-screen p-4">
        <Navbar />
        <IngredientModeSwitcher />

        {/* Background */}
        <div className="fixed inset-0 -z-10 pointer-events-none">
          <div className="absolute inset-0"></div>
        </div>

        {/* Content */}
        <div className="max-w-[520px] mx-auto p-6 bg-gray-700 border border-green-600 rounded-2xl shadow-lg text-white">
          <h1 className="text-2xl font-semibold mb-4">
            Add ingredient from a batch
          </h1>
          {/* Extras selector */}
          <div className="mt-3">
            <button
              type="button"
              onClick={() => setShowExtras((v) => !v)}
              className="px-3 py-1.5 text-sm border border-green-600 rounded-lg bg-gray-600 hover:bg-gray-500 transition"
            >
              {showExtras ? "Hide extras" : "+ Add nutrients"}
            </button>

            {showExtras && (
              <div className="mt-3 border border-green-600 p-3 rounded-lg bg-gray-600 space-y-1">
                {EXTRA_NUTRIENTS.map((n) => (
                  <label
                    key={n.key}
                    className="flex items-center gap-2 cursor-pointer text-sm"
                  >
                    <input
                      type="checkbox"
                      checked={selected.includes(n.key)}
                      onChange={() => toggleExtra(n.key)}
                      className="accent-green-600"
                    />
                    {n.label}
                  </label>
                ))}
              </div>
            )}
          </div>
          {/* Form */}
          <form onSubmit={onSubmit} className="grid gap-3 mt-4">
            {/* Name */}
            <input
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />

            {/* Priority */}
            <select
              value={priorityUser}
              onChange={(e) => setPriorityUser(e.target.value)}
              required
              className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="">Priority</option>
              <option value={0}>Supporting ingredient</option>
              <option value={1}>Main ingredient</option>
            </select>

            {/* Total weight */}
            <input
              type="number"
              min="1"
              step="any"
              placeholder="Final meal weight (g)"
              value={totalWeightG}
              onChange={(e) => setTotalWeightG(e.target.value)}
              required
              className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />

            {/* Nutrient inputs */}
            {selected.map((key) => {
              const meta = ALL.find((n) => n.key === key);

              return (
                <input
                  key={key}
                  type="number"
                  min="0"
                  step="any"
                  placeholder={`${meta.label} (TOTAL)`}
                  value={values[key] ?? ""}
                  onChange={(e) => setNutrientValue(key, e.target.value)}
                  required
                  className="w-full px-3 py-2 bg-gray-800 border border-green-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              );
            })}

            <button
              type="submit"
              disabled={loading}
              className="mt-2 py-2 px-4 rounded-lg bg-green-600 border border-green-600 text-white font-medium hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {loading ? "Sending..." : "Save ingredient!"}
            </button>
          </form>
          {result && (
            <p className="text-white font-medium">Saved successfully!</p>
          )}{" "}
          {error && (
            <>
              <p className="text-white font-medium">
                Error has occured or ingredient already exists.
              </p>
              <p className="text-white font-medium">Please try again later.</p>
            </>
          )}
        </div>
      </main>
    </ProtectedPage>
  );
}
