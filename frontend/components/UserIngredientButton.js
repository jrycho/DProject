"use client";
import { useEffect, useState } from "react";
import { deleteIngredientFromTempLog, setAmountInTemp } from "@/utils/userFunctionsTempLog";


export default function UserIngredientButton({ data, onRemove }) {
  const {
    name,
    kcal,
    protein,
    carbs,
    fat,
    barcode,
    amount: initialAmount,
  } = data ?? {};

  const label = `${kcal} kcal/100 g • ${protein} g Protein • ${carbs} g Carbs • ${fat} g Fats`;

  const [amount, setAmount] = useState(String(initialAmount ?? 0));
  const [saving, setSaving] = useState(false);

  // prevent values reset on API reloads
  useEffect(() => {
    setAmount(String(initialAmount ?? 0));
  }, [initialAmount]);

  const handleChange = (e) => {
    const value = e.target.value; // string

    // Allow empty while typing
    if (value === "") {
      setAmount("");
      return;
    }

    // Only digits (grams)
    if (/^\d+$/.test(value)) {
      setAmount(value);
    }
  };

  const handleBlurAmount = async () => {
    const finalValue = amount === "" ? "0" : amount;

    if (finalValue !== amount) setAmount(finalValue);

    const num = Number(finalValue);


    try {
     setSaving(true);
    await setAmountInTemp(barcode, num);
     } catch (e) {
       console.error("Failed to save amount:", e);
     } finally {
       setSaving(false);
     }

    void num; // avoid lint if update is not used
  };

  const handleRemove = async () => {
    // Let parent do optimistic UI if it wants; still safe if parent just refetches.
    try {
      await deleteIngredientFromTempLog(barcode);
    } catch (e) {
      console.error("Failed to delete ingredient:", e);
      // parent can also show toast based on error if desired
    } finally {
      onRemove?.(barcode);
    }
  };

  return (
    <div className=" w-full h-29 relative">
      <div
        className="bg-gray-600 border-green-600 border rounded-xl shadow-sm
               hover:bg-gray-500 active:scale-[0.98]
               focus-within:ring-2 focus-within:ring-offset-2
               flex items-center justify-between
               px-5 py-3 text-sm text-white font-sans h-full"
      >
        {/* Left - Info */}
        <div className="flex flex-col gap-1 max-w-[60%]">
          <span className="truncate font-medium">{name}</span>
          <span className="text-xs text-gray-300">{label}</span>
        </div>

        {/* Right - Amount */}
        <div className="flex flex-col gap-1 text-xs text-gray-200">
          <label className="text-gray-300">Amount (g)</label>

          <input
            type="number"
            inputMode="numeric"
            pattern="[0-9]*"
            min="0"
            value={amount}
            onChange={handleChange}
            onBlur={handleBlurAmount}
            onFocus={(e) => e.target.select()}
            disabled={saving}
            className="w-24 px-2 py-1 rounded bg-gray-700
                     text-white text-sm border border-gray-500
                     focus:outline-none focus:ring-2 focus:ring-green-500 [appearance:textfield]
                     disabled:opacity-60"
            placeholder="g"
          />
        </div>
      </div>

      {/* Remove (X) */}
      <button
        type="button"
        onClick={handleRemove}
        className="absolute -top-2 -right-2 bg-red-500
               w-6 h-6 rounded-full text-xs
               flex items-center justify-center
               hover:bg-red-600"
        aria-label={`Remove ${name}`}
        title={`Remove ${name}`}
      >
        X
      </button>
    </div>
  );
}
