"use client";
import IngredientButton from "@/components/IngredientButton";
import { fetchIngredientButtons } from "@/utils/fetchIngredientButtons";
import { useEffect, useState } from "react";
import { deleteIngredient } from "@/utils/deleteIngredient";


export default function TestPage() {
  const data = { id: 1, name: "Chicken breast 100g", kcal: 165, protein: 31, carbs: 0, fat: 3.6 };
  const label = `${data.kcal} kcal • ${data.protein}P/${data.carbs}C/${data.fat}F`;
  const mealId = "8432904e-186c-4119-a094-d3c7d910014b";
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
   console.log("[TestPage] render")




    useEffect(() => {
      console.log("effect")
    let cancelled = false;
    (async () => {
      try {
        const data = await fetchIngredientButtons(mealId)
        console.log(data);
        if (!cancelled) setItems(data);
      } catch (e) {
        if (!cancelled) setError(e);
      }
    })();
    return () => { cancelled = true; };
  }, [mealId]);


    const handleRemove = async (barcode) => {
    // optional: optimistic UI
    setItems((prev) => prev.filter((x) => x.barcode !== barcode));
    try {
      await deleteIngredient(mealId, barcode);
    } finally {
; // ensure fresh list from server
    }
  };

  return (
    <div className="flex flex-col gap-2 ">
      {items.map(it => (
        <IngredientButton key={it.name} data={it} onRemove={()=>handleRemove(it.barcode)}/>
      ))}
      {items.length === 0 && <p className="text-sm text-gray-500">No ingredients.</p>}
    </div>
  );
}