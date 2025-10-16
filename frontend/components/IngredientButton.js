'use client'
import { deleteIngredient } from "@/utils/deleteIngredient";

export default function IngredientButton({ data, onRemove }) {
    
  const { id, name, kcal, protein, carbs, fat } = data; // no fallbacks needed
  const label = `${kcal} kcal/100 g
   • ${protein} g Protein
    • ${carbs} g Carbs
     • ${fat} g Fats`;



return(
    <>
    <button
        type="button"
        onClick={() => onRemove?.(id)}
        title={`Remove ${name}`}
        aria-label={`Remove ${name} (${label})`}
        className="bg-gray-600  border-green-600 rounded-full border shadow-sm hover:bg-gray-500 active:scale-[0.98] 
        focus:outline-none focus:ring-2 focus:ring-offset-2
        
        inline-flex flex-col  gap-2 justify-center                  
        px-5 py-3 text-sm  text-white font-sans
        
        w-100 h-20"
    >
      <span className="font-sans truncate  ">{name}</span>
      <span className="text-xs text-gray-300 items-start">{label}</span>
    </button>
    </>
);
}
