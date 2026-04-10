import { optimizeFunction } from "@/utils/optimizeFunction";
import { useState, useCallback } from "react";
import { useMealId } from "@/utils/mealIdCtx";

export default function OptimizeButton({ mealId, mealType, onResults }) {
  const [busy, setBusy] = useState(false);
  const disabled = busy || !mealId;
  const [mealWeights, setMealWeights] = useState({});
  const [mealMacros, setMealMacros] = useState({});
  const hasActiveMeal = Boolean(mealId);

  const handleOptimize = useCallback(async () => {
    if (!mealId || busy) return;
    const id = mealId; // prefer context, fallback to prop
    if (!id || busy) return; // guard: no id or already running

    try {
      setBusy(true);
      const { weights, macros } = await optimizeFunction(id, mealType);
      setMealMacros(macros);
      setMealWeights(weights);
      console.log(mealMacros, mealWeights);
      onResults?.({ mealWeights: weights, mealMacros: macros });
    } finally {
      setBusy(false);
    }
  });
  return (
    <div
      className={`${
        hasActiveMeal ? "fixed flex" : "hidden"
      } inset-x-0 bottom-4 z-[90] justify-center px-4 md:static md:block md:px-0`}
    >
      <button
        className="w-full max-w-md md:w-[18rem] md:max-w-none md:ml-30 min-h-10 bg-green-600 border border-green-900 rounded-tl-xl rounded-br-xl hover:bg-green-700 disabled:bg-green-900 shadow-lg md:shadow-none"
        onClick={handleOptimize}
        disabled={disabled}
      >
        Optimize
      </button>
    </div>
  );
}
