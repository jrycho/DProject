"use client";
import { deleteIngredient } from "@/utils/deleteIngredient";
import { useEffect, useState } from "react";
import { updateIngredientValues } from "@/utils/updateIngredientValues";

export default function IngredientButton({
  data,
  mealId,
  onRemove,
  onChangeAmount,
  onChangePieceWeight,
}) {
  const {
    name,
    kcal,
    protein,
    carbs,
    fat,
    barcode,
    set_amount = 0,
    piece_weight = 0,
  } = data;
  const label = `${kcal} kcal/100 g
   • ${protein} g Protein
    • ${carbs} g Carbs
     • ${fat} g Fats`;
  const [amount, setAmount] = useState(String(set_amount));
  const [pieceWeight, setPieceWeight] = useState(String(piece_weight));


//prevent values on API relods
useEffect(() => {
  setAmount(String(set_amount ?? 0));
  setPieceWeight(String(piece_weight ?? 0));
}, [set_amount, piece_weight]);

  const handleChange = (e) => {
    const value = e.target.value; // string

    // Allow empty while typing
    if (value === "") {
      setAmount("");
      onChangeAmount?.(id, 0);
      return;
    }

    // Only digits
    if (/^\d+$/.test(value)) {
      setAmount(value);
      onChangeAmount?.(id, Number(value));
    }
  };

  const handleBlurAmount = async () => {
    const finalValue = amount === "" ? "0" : amount;

    // Normalize UI
    if (finalValue !== amount) {
      setAmount(finalValue);
    }

    const num = Number(finalValue);

    // Optional parent update
    onChangeAmount?.(id, num);

    // Save to backend
    try {
      await updateIngredientValues(
        barcode,
        mealId,
        num,
        Number(pieceWeight || 0),
      );
    } catch (e) {
      console.error("Failed to save amount:", e);
    }
  };

  const handlePieceWeightChange = (e) => {
    const value = e.target.value; // string

    if (value === "") {
      setPieceWeight("");
      onChangePieceWeight?.(id, 0);
      return;
    }

    if (/^\d+$/.test(value)) {
      setPieceWeight(value);
      onChangePieceWeight?.(id, Number(value));
    }
  };

  const handleBlurPieceWeight = async () => {
    // If user left the input empty, replace it with "0"
    const finalValue = pieceWeight === "" ? "0" : pieceWeight;
    // If we changed "" → "0", update the UI
    if (finalValue !== pieceWeight) {
      setPieceWeight(finalValue);
    }
    // Convert string to number for backend / parent
    const num = Number(finalValue);
    // Notify parent component about change
    onChangePieceWeight?.(id, num);

    try {
      // Save both values to backend
      // We send:
      // - current forced amount (grams)
      // - new piece weight (grams per piece)
      await updateIngredientValues(barcode, mealId, Number(amount || 0), num);
    } catch (e) {
      console.error("Failed to save piece weight:", e);
    }
  };
  return (
    <>
      {/*   <div>
    <button
        type="button"
        onClick={() => onRemove?.(id)}
        title={`Remove ${name}`}
        aria-label={`Remove ${name} (${label})`}
        className="bg-gray-600  border-green-600 border rounded-xl shadow-sm hover:bg-gray-500 active:scale-[0.98] 
        focus:outline-none focus:ring-2 focus:ring-offset-2
        
        inline-flex flex-col  gap-2 justify-center                  
        px-5 py-3 ml-14 text-sm  text-white font-sans
        
        w-100 h-20"
    >
      <span className="font-sans truncate  ">{name}</span>
      <span className="text-xs text-gray-300 items-start">{label}</span>
    </button>
        <input
        type="number"
        min="1"
        value={amount}
        onChange={handleChange}
        className="w-20 px-2 py-1 rounded border border-gray-500
                   bg-gray-700 text-white text-sm
                   focus:outline-none focus:ring-2 focus:ring-green-500"
        placeholder="g"
      />
    </div>*/}

      <div className="ml-14 w-100 h-29 relative">
        <div
          className="bg-gray-600 border-green-600 border rounded-xl shadow-sm
               hover:bg-gray-500 active:scale-[0.98]
               focus-within:ring-2 focus-within:ring-offset-2
               flex items-center justify-between
               px-5 py-3 text-sm text-white font-sans h-full"
        >
          {/* Left side - Info */}
          <div className="flex flex-col gap-1 max-w-[60%]">
            <span className="truncate font-medium">{name}</span>
            <span className="text-xs text-gray-300">{label}</span>
          </div>

          {/* Right side - Inputs */}
          <div className="flex flex-col gap-2 text-xs text-gray-200">
            {/* Amount */}
            <div className="flex flex-col gap-1">
              <label className="text-gray-300">Set amount</label>

              <input
                type="number"
                inputMode="numeric"
                pattern="[0-9]*"
                min="1"
                value={amount}
                onChange={handleChange}
                onBlur={handleBlurAmount}
                onFocus={(e) => e.target.select()}
                className="w-24 px-2 py-1 rounded bg-gray-700
                     text-white text-sm border border-gray-500
                     focus:outline-none focus:ring-2 focus:ring-green-500 [appearance:textfield]"
                placeholder="g"
              />
            </div>

            {/* Weight per piece */}
            <div className="flex flex-col gap-1">
              <label className="text-gray-300">Weight of piece</label>

              <input
                type="number"
                min="1"
                value={pieceWeight}
                onChange={handlePieceWeightChange}
                onBlur={handleBlurPieceWeight}
                className="w-24 px-2 py-1 rounded bg-gray-700
                     text-white text-sm border border-gray-500
                     focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="g"
              />
            </div>
          </div>
        </div>

        {/* Remove Button */}
        <button
          type="button"
          onClick={() => onRemove?.(barcode)}
          className="absolute -top-2 -right-2 bg-red-500
               w-6 h-6 rounded-full text-xs
               flex items-center justify-center
               hover:bg-red-600"
        >
          X
        </button>
      </div>
    </>
  );
}
