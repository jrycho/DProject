"use client";
import { useEffect, useState } from "react";
import { updateIngredientValues } from "@/utils/updateIngredientValues";

export default function IngredientButton({ data, mealId, onRemove }) {
  const {
    name,
    kcal,
    protein,
    carbs,
    fat,
    barcode,
    set_amount = 0,
    piece_weight = 0,
    min_amount = 0,
    max_amount = 0,
  } = data;

  const label = `${kcal} kcal/100 g | ${protein} g protein | ${carbs} g carbs | ${fat} g fats`;
  const [amount, setAmount] = useState(String(set_amount));
  const [pieceWeight, setPieceWeight] = useState(String(piece_weight));
  const [minAmount, setMinAmount] = useState(String(min_amount));
  const [maxAmount, setMaxAmount] = useState(String(max_amount));

  useEffect(() => {
    setAmount(String(set_amount ?? 0));
    setPieceWeight(String(piece_weight ?? 0));
    setMinAmount(String(min_amount ?? 0));
    setMaxAmount(String(max_amount ?? 0));
  }, [set_amount, piece_weight, min_amount, max_amount]);

  const handleNumericChange = (setter) => (e) => {
    const value = e.target.value;
    if (value === "") {
      setter("");
      return;
    }

    if (/^\d+$/.test(value)) {
      setter(value);
    }
  };

  const normalizeValue = (value, setter) => {
    const normalized = value === "" ? "0" : value;
    setter(normalized);
    return Number(normalized);
  };

  const persistValues = async (nextValues) => {
    try {
      await updateIngredientValues({
        barcode,
        mealId,
        ...nextValues,
      });
    } catch (e) {
      console.error("Failed to save ingredient values:", e);
    }
  };

  const handleBlur = async (field) => {
    const nextAmount = field === "amount" ? normalizeValue(amount, setAmount) : Number(amount || 0);
    const nextPieceWeight =
      field === "pieceWeight"
        ? normalizeValue(pieceWeight, setPieceWeight)
        : Number(pieceWeight || 0);
    const nextMinAmount =
      field === "minAmount" ? normalizeValue(minAmount, setMinAmount) : Number(minAmount || 0);
    const nextMaxAmount =
      field === "maxAmount" ? normalizeValue(maxAmount, setMaxAmount) : Number(maxAmount || 0);

    if (nextMaxAmount > 0 && nextMinAmount > nextMaxAmount) {
      if (field === "minAmount") {
        setMaxAmount(String(nextMinAmount));
        await persistValues({
          setAmount: nextAmount,
          pieceWeight: nextPieceWeight,
          minAmount: nextMinAmount,
          maxAmount: nextMinAmount,
        });
      } else if (field === "maxAmount") {
        setMinAmount(String(nextMaxAmount));
        await persistValues({
          setAmount: nextAmount,
          pieceWeight: nextPieceWeight,
          minAmount: nextMaxAmount,
          maxAmount: nextMaxAmount,
        });
      }
      return;
    }

    await persistValues({
      setAmount: nextAmount,
      pieceWeight: nextPieceWeight,
      minAmount: nextMinAmount,
      maxAmount: nextMaxAmount,
    });
  };

  return (
    <div className="relative mx-2 w-full max-w-[24rem] self-center md:mx-0 md:max-w-none">
      <div className="grid gap-4 rounded-2xl border border-green-600 bg-gray-600 px-4 py-4 text-sm text-white shadow-sm transition hover:bg-gray-500 focus-within:ring-2 focus-within:ring-green-400 md:grid-cols-[minmax(0,1fr)_auto]">
        <div className="min-w-0">
          <span className="block truncate text-sm font-semibold">{name}</span>
          <span className="mt-1 block text-xs leading-5 text-gray-200">{label}</span>
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs text-gray-200 sm:w-[14rem]">
          <label className="flex flex-col gap-1">
            <span className="text-gray-300">Set amount</span>
            <input
              type="number"
              inputMode="numeric"
              pattern="[0-9]*"
              value={amount}
              onChange={handleNumericChange(setAmount)}
              onBlur={() => handleBlur("amount")}
              onFocus={(e) => e.target.select()}
              className="w-full rounded-lg border border-gray-500 bg-gray-700 px-2 py-1.5 text-sm text-white [appearance:textfield] focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="g"
            />
          </label>

          <label className="flex flex-col gap-1">
            <span className="text-gray-300">Piece weight</span>
            <input
              type="number"
              inputMode="numeric"
              pattern="[0-9]*"
              value={pieceWeight}
              onChange={handleNumericChange(setPieceWeight)}
              onBlur={() => handleBlur("pieceWeight")}
              onFocus={(e) => e.target.select()}
              className="w-full rounded-lg border border-gray-500 bg-gray-700 px-2 py-1.5 text-sm text-white [appearance:textfield] focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="g"
            />
          </label>

          <label className="flex flex-col gap-1">
            <span className="text-gray-300">Min weight</span>
            <input
              type="number"
              inputMode="numeric"
              pattern="[0-9]*"
              value={minAmount}
              onChange={handleNumericChange(setMinAmount)}
              onBlur={() => handleBlur("minAmount")}
              onFocus={(e) => e.target.select()}
              className="w-full rounded-lg border border-gray-500 bg-gray-700 px-2 py-1.5 text-sm text-white [appearance:textfield] focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="g"
            />
          </label>

          <label className="flex flex-col gap-1">
            <span className="text-gray-300">Max weight</span>
            <input
              type="number"
              inputMode="numeric"
              pattern="[0-9]*"
              value={maxAmount}
              onChange={handleNumericChange(setMaxAmount)}
              onBlur={() => handleBlur("maxAmount")}
              onFocus={(e) => e.target.select()}
              className="w-full rounded-lg border border-gray-500 bg-gray-700 px-2 py-1.5 text-sm text-white [appearance:textfield] focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="g"
            />
          </label>
        </div>
      </div>

      <button
        type="button"
        onClick={() => onRemove?.(barcode)}
        className="absolute -right-2 -top-2 flex h-7 w-7 items-center justify-center rounded-full bg-red-500 text-xs text-white hover:bg-red-600"
      >
        X
      </button>
    </div>
  );
}
