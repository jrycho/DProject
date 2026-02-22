"use client";
import { useEffect, useState } from "react";
import IngredientSearchBar from "@/components/IngredientSearchBar";
import { deleteIngredient } from "@/utils/deleteIngredient";
import { fetchIngredientButtons } from "@/utils/fetchIngredientButtons";
import IngredientButton from "./IngredientButton";
import UserIngredientSearchbarComponent from "./UserIngredientSearchbar";
import { addIngredient } from "@/utils/ingredientAdd";

export default function MealButton({
  meal,
  isLogged,
  onClick,
  isActive,
  mealId,
}) {
  const data = {
    id: 1,
    name: "Chicken breast 100g",
    kcal: 165,
    protein: 31,
    carbs: 0,
    fat: 3.6,
  };
  const label = `${data.kcal} kcal • ${data.protein}P/${data.carbs}C/${data.fat}F`;
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [reloadTick, setReloadTick] = useState(0);
  const [useUserDb, setUseUserDb] = useState(false);
  // when set to reload or when mealId is changed, reload
  useEffect(() => {
    if (mealId == null || mealId === "") {
      setItems([]);
      setError(null);
      return;
    }

    console.log("effect");
    let cancelled = false;
    (async () => {
      try {
        const data = await fetchIngredientButtons(mealId);
        console.log(data);
        if (!cancelled) setItems(data);
      } catch (e) {
        if (!cancelled) setError(e);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [mealId, reloadTick]);

  const handleRemove = async (barcode) => {
    // optional: optimistic UI
    setItems((prev) => prev.filter((x) => x.barcode !== barcode));
    try {
      await deleteIngredient(mealId, barcode);
      setReloadTick((t) => t + 1);
    } catch (e) {
      setError(e);
      setReloadTick((t) => t + 1);
    }
  };

  return (
    <div className="w-full">
      <button
        onClick={onClick}
        className={`w-130 ml-10 mr-10 px-4 py-2 text-white transition duration-300 border 
        ${
          isActive
            ? // ✅ CHANGED: pb-00 -> pb-0, and remove bottom rounding so it touches the panel
              "pt-2 pb-0 bg-gray-600 hover:bg-gray-500 rounded-t-xl rounded-b-none border-green-600"
            : isLogged
              ? "py-2 bg-gray-600 hover:bg-gray-500 rounded-xl border-green-600"
              : "py-2 bg-gray-700 hover:bg-gray-500 rounded-xl border-green-600"
        }
      `}
      >
        {isLogged ? `${meal} (Logged)` : meal}
      </button>

      <div
        className={`ml-10 mr-10 w-130 bg-gray-500 border border-green-600 rounded-b-2xl
    transition-[height,opacity] duration-300
    ${isActive ? "h-[26rem] opacity-100 -mt-px" : "h-0 opacity-0"}
    overflow-hidden
  `}
      >
        {/* ✅ CHANGED: add padding so content doesn’t touch edges */}
        <div className="h-full flex flex-col min-h-0 px-3 pb-3">
          {/* top toggle buttons */}
          <div className="flex gap-2 pt-2">
            <button
              onClick={() => setUseUserDb(false)}
              className={`px-3 py-1 rounded text-sm ${
                !useUserDb ? "bg-green-600 text-white" : "bg-gray-400"
              }`}
            >
              Find ingredients
            </button>

            <button
              onClick={() => setUseUserDb(true)}
              className={`px-3 py-1 rounded text-sm ${
                useUserDb ? "bg-green-600 text-white" : "bg-gray-400"
              }`}
            >
              My ingredients
            </button>
          </div>

          {/* search area */}
          <div className="mt-2">
            {useUserDb ? (
              <UserIngredientSearchbarComponent
                isActive={isActive}
                mealId={mealId}
                onAdded={() => setReloadTick((t) => t + 1)}
                addIngredientFunction={async (item, mealIdArg) => {
                  await addIngredient(item.code, mealIdArg);
                }}
              />
            ) : (
              <IngredientSearchBar
                isActive={isActive}
                mealId={mealId}
                onAdded={() => setReloadTick((t) => t + 1)}
                addIngredientFunction={async (barcode, mealIdArg) => {
                  await addIngredient(barcode, mealIdArg);
                }}
              />
            )}
          </div>

          {/* ingredients buttons */}

          <div className="mt-2 flex-1 min-h-0 overflow-y-auto overflow-x-visible flex flex-col gap-2 pr-2 pt-2 custom-scrollbar">
            {items.map((it) => (
              <IngredientButton
                key={it.name}
                data={it}
                mealId={mealId}
                onRemove={() => handleRemove(it.barcode)}
              />
            ))}
            {items.length === 0 && (
              <p className="text-sm text-gray-300">No ingredients.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
