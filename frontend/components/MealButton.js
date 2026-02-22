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
        className={`w-130 ml-10 mr-10 px-4 py-2  text-white transition duration-300 border 
        ${
          isActive
            ? "pt-2 pb-00 bg-gray-600  hover:bg-gray-500 rounded-t-xl border-green-600  "
            : isLogged
              ? "py-2 bg-gray-600  hover:bg-gray-500 rounded-xl border-green-600"
              : "py-2  bg-gray-700 hover:bg-gray-500 rounded-xl  border-green-600"
        }
      `}
      >
        {isLogged ? `${meal} (Logged)` : meal}
      </button>
      <div
        className={`overflow-hidden transition-all duration-300 ml-10 mr-10 w-130 rounded-br-bl  bg-gray-500 rounded-b-2xl
              ${isActive ? "min-h-30 max-h-90 opacity-100" : "max-h-0 opacity-0  "}
            `}
      >
        <div className="flex gap-2 mb-0 ml-10 mt-2">
          <button
            onClick={() => setUseUserDb(false)}
            className={`px-3 py-1 rounded text-sm ${
              !useUserDb ? "bg-green-600 text-white " : "bg-gray-400 "
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
        <div className={`  text-white transition duration-300  bg-gray-500`}>
          <div>
            {useUserDb ? (
              <UserIngredientSearchbarComponent
                isActive={isActive}
                mealId={mealId}
                onAdded={() => setReloadTick((t) => t + 1)}
                addIngredientFunction={async (item, mealIdArg) => {
                  // map your search result → barcode/code
                  await addIngredient(item.code, mealIdArg);
                }}
              />
            ) : (
              <IngredientSearchBar
                isActive={isActive}
                mealId={mealId}
                onAdded={() => setReloadTick((t) => t + 1)}
                addIngredientFunction={async (barcode, mealIdArg) => {
                  // map your search result → barcode/code
                  await addIngredient(barcode, mealIdArg);
                }}
              />
            )}
            {/*ingredients buttons */}
            <div className="flex flex-col gap-2 ">
              {items.map((it) => (
                <IngredientButton
                  key={it.name}
                  data={it}
                  mealId={mealId}
                  onRemove={() => handleRemove(it.barcode)}
                />
              ))}
              {items.length === 0 && (
                <p className="text-sm text-gray-500">No ingredients.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
