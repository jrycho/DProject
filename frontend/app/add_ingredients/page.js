// app/ingredients/add-macros/page.jsx
"use client";

import { useState } from "react";
import { addUserIngredientDirect } from "@/utils/userIngredientDirectMacros";
import ProtectedPage from "@/components/ProtectedPage";
import Threads from "@/components/Threads";
import Navbar from "@/components/Navbar";
import ThreadsBackground from "@/components/ThreadsBackground";
import { CORE_NUTRIENTS, EXTRA_NUTRIENTS } from "@/utils/userIngredientsNutrientsConfig";
import IngredientModeSwitcher from "@/components/UserIngredientSwitcher";

export default function AddMacrosSimple() {
  /* Basic */
  const [name, setName] = useState("");
  const [priorityUser, setPriorityUser] = useState("");

  /* Selected nutrients (core always included) */
  const [selected, setSelected] = useState(
    CORE_NUTRIENTS.map((n) => n.key)
  );

  /* Nutrient values */
  const [values, setValues] = useState({});

  /* UI state */
  const [showExtras, setShowExtras] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function toggleExtra(key) {
    setSelected((prev) =>
      prev.includes(key)
        ? prev.filter((k) => k !== key)
        : [...prev, key]
    );
  }

  function setNutrientValue(key, val) {
    setValues((prev) => ({
      ...prev,
      [key]: val,
    }));
  }

  async function onSubmit(e) {
    e.preventDefault();

    setError("");
    setResult(null);
    setLoading(true);

    /* Build nutriments dynamically */
    const nutriments = {};

    selected.forEach((key) => {
      nutriments[key] = Number(values[key] ?? 0);
    });

    const payload = {
      product_name: name,
      priority_user: priorityUser,
      nutriments,
      categories_tags: ["custom"],
    };

    try {
      const data = await addUserIngredientDirect(payload);

      setResult(data);

      // Reset
      setName("");
      setValues({});
      setSelected(CORE_NUTRIENTS.map((n) => n.key));
    } catch (err) {
      setError(err.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  const ALL = [...CORE_NUTRIENTS, ...EXTRA_NUTRIENTS];

  return (
<ProtectedPage>
  <main className="relative min-h-screen p-4 ">
    <Navbar />
    <IngredientModeSwitcher/>

    {/* Background */}
    <div className="fixed inset-0 -z-10 pointer-events-none">
      <div className="absolute inset-0">
      </div>
    </div>

    {/* Content */}
    <div className="max-w-[520px] mx-auto p-6 bg-gray-700 backdrop-blur rounded-lg shadow">
      <h1 className="text-2xl font-semibold mb-4">
        Add ingredient (macros)
      </h1>

      {/* Extras selector */}
      <div className="mt-3">
        <button
          type="button"
          onClick={() => setShowExtras((v) => !v)}
          className="px-3 py-1.5 text-sm border rounded hover:bg-gray-600 transition"
        >
          {showExtras ? "Hide extras" : "+ Add nutrients"}
        </button>

        {showExtras && (
          <div className="mt-2 border border-gray-300 p-3 rounded-md bg-gray-500 space-y-1">
            {EXTRA_NUTRIENTS.map((n) => (
              <label
                key={n.key}
                className="flex items-center gap-2 cursor-pointer text-sm"
              >
                <input
                  type="checkbox"
                  checked={selected.includes(n.key)}
                  onChange={() => toggleExtra(n.key)}
                  className="accent-blue-600"
                />
                {n.label}
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Form */}
      <form
        onSubmit={onSubmit}
        className="grid gap-3 mt-4"
      >
        {/* Name */}
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-200"
        />

        {/* Priority */}
        <input
          type="number"
          min="0"
          step="1"
          placeholder="Priority"
          value={priorityUser}
          onChange={(e) => setPriorityUser(e.target.value)}
          required
          className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-200"
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
              placeholder={meta.label}
              value={values[key] ?? ""}
              onChange={(e) =>
                setNutrientValue(key, e.target.value)
              }
              required
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-200"
            />
          );
        })}

        <button
          type="submit"
          disabled={loading}
          className="mt-2 py-2 px-4 rounded bg-gray-600 border border-gray-200 text-white font-medium hover:bg-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </form>



      {/* Error */}
      {error && (
        <>
          <h2 className="mt-4 text-lg font-semibold text-red-600">
            Error
          </h2>

          <pre className="mt-2 bg-red-100 text-red-800 p-3 rounded text-sm overflow-auto">
            {error}
          </pre>
        </>
      )}

      {/* Result */}
      {result && (
        <>
          <h2 className="mt-4 text-lg font-semibold text-green-600">
            Response
          </h2>

          <pre className="mt-2 bg-green-100 text-green-800 p-3 rounded text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </>
      )}
    </div>
  </main>
</ProtectedPage>
  );}