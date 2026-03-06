// app/ingredients/temp-log/page.jsx
"use client";

import { useEffect, useMemo, useState } from "react";
import ProtectedPage from "@/components/ProtectedPage";
import Navbar from "@/components/Navbar";
import IngredientModeSwitcher from "@/components/UserIngredientSwitcher";

import IngredientSearchBar from "@/components/IngredientSearchBar";
import UserIngredientSearchbarComponent from "@/components/UserIngredientSearchbar";

import UserIngredientButton from "@/components/UserIngredientButton";

import {
  addIngredientToTempLog,
  fetchTempIngredientButtons,
  saveTempLogToPermanent,
} from "@/utils/userFunctionsTempLog";

export default function TempLogPage() {
  // UI state
  const [useUserDb, setUseUserDb] = useState(false);
  const [items, setItems] = useState([]);
  const [reloadTick, setReloadTick] = useState(0);

  // Save-to-perm form (keep minimal, like your add-macros page style)
  const [name, setName] = useState("");
  const [priorityUser, setPriorityUser] = useState("0");

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  // Fetch temp items
  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        setError("");
        setLoading(true);
        const data = await fetchTempIngredientButtons();
        if (!cancelled)
          setItems(Array.isArray(data) ? data : (data?.items ?? []));
      } catch (e) {
        if (!cancelled)
          setError(e?.message || "Failed to load temp ingredients");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [reloadTick]);


  async function onSave(e) {
    e.preventDefault();
    setError("");
    setResult(null);

    // Basic guard: don’t save empty
    if (!items.length) {
      setError("No ingredients in temp log.");
      return;
    }

    setSaving(true);
    try {

      const payload = {
        product_name: name || "Temp meal",
        priority_user: Number(priorityUser || 0),
        categories_tags: ["temp_log"],
      };

      const data = await saveTempLogToPermanent(payload);
      setResult(data);

      // Clear UI
      setName("");
      setPriorityUser("0");
      setItems([]);
      setReloadTick((t) => t + 1);
    } catch (err) {
      setError(err?.message || "Save failed");
    } finally {
      setSaving(false);
    }
  }

  return (
    <ProtectedPage>
      <main className="relative min-h-screen p-4 ">
        <Navbar />
        <IngredientModeSwitcher />

        {/* Content */}
        <div className="max-w-[520px] mx-auto p-6 bg-gray-700 backdrop-blur rounded-lg shadow">
          <h1 className="text-2xl font-semibold mb-4">Build meal (temp log)</h1>

          {/* Mode switch */}
          <div className="flex gap-2 mb-4">
            <button
              type="button"
              onClick={() => setUseUserDb(false)}
              className={`px-3 py-1 rounded text-sm ${
                !useUserDb ? "bg-green-600 text-white" : "bg-gray-400"
              }`}
            >
              Find ingredients
            </button>

            <button
              type="button"
              onClick={() => setUseUserDb(true)}
              className={`px-3 py-1 rounded text-sm ${
                useUserDb ? "bg-green-600 text-white" : "bg-gray-400"
              }`}
            >
              My ingredients
            </button>
          </div>

          {/* Search */}
          <div className="mb-4">
            {useUserDb ? (
              <UserIngredientSearchbarComponent
                isActive={true}
                // mealId not needed for temp-log backend; component can ignore it
                mealId={""}
                onAdded={() => setReloadTick((t) => t + 1)}
                addIngredientFunction={async (item, mealIdArg) => {
                  // map search result → barcode/code
                  await addIngredientToTempLog(item.code, mealIdArg);
                }}
              />
            ) : (
              <IngredientSearchBar
                isActive={true}
                mealId={""}
                onAdded={() => setReloadTick((t) => t + 1)}
                addIngredientFunction={async (barcode, mealIdArg) => {
                  // map search result → barcode/code
                  await addIngredientToTempLog(barcode, mealIdArg);
                }}
              />
            )}
          </div>

          {/* List */}
          <div className="flex flex-col gap-2">
            {loading && (
              <p className="text-sm text-gray-200">Loading ingredients…</p>
            )}

            {!loading &&
              items.map((it) => (
                <UserIngredientButton
                  key={it?.barcode || it?.name}
                  data={it}
                  onRemove={() => setReloadTick((t) => t + 1)}
                />
              ))}

            {!loading && items.length === 0 && (
              <p className="text-sm text-gray-300">No ingredients.</p>
            )}
          </div>



          {/* Save-to-perm (add-macros style) */}
          <h2 className="mt-6 text-lg font-semibold">Save to permanent DB</h2>

          <form onSubmit={onSave} className="grid gap-3 mt-3">
            <input
              placeholder="Meal name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-200"
            />

            <input
              type="number"
              min="0"
              step="1"
              placeholder="Priority"
              value={priorityUser}
              onChange={(e) => setPriorityUser(e.target.value)}
              className="w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-200"
            />

            <button
              type="submit"
              disabled={saving || !items.length}
              className="mt-1 py-2 px-4 rounded bg-gray-600 border border-gray-200 text-white font-medium hover:bg-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {saving ? "Saving..." : "Save meal"}
            </button>
          </form>



          {/* Error */}
          {error && (
            <>
              <h2 className="mt-4 text-lg font-semibold text-red-600">Error</h2>
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
  );
}
