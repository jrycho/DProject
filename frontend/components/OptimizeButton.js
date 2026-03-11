import { optimizeFunction } from "@/utils/optimizeFunction";
import { useState, useCallback } from "react";
import { useMealId } from "@/utils/mealIdCtx";

export default function OptimizeButton({ mealId, mealType, onResults }) {
  const [busy, setBusy] = useState(false);
  const disabled = busy || !mealId;
  const [mealWeights, setMealWeights] = useState({});
  const [mealMacros, setMealMacros] = useState({});

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
    <div>
      <button
        className="w-full md:w-[18rem] md:ml-30 min-h-10 bg-green-600 border border-green-900 rounded-tl-xl rounded-br-xl hover:bg-green-700 disabled:bg-green-900"
        onClick={handleOptimize}
        disabled={disabled}
      >
        Optimize
      </button>
    </div>
  );
}
