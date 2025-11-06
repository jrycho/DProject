'use client'
import { useEffect, useState } from "react";
import IngredientSearchBar from '@/components/IngredientSearchBar';
import { deleteIngredient } from "@/utils/deleteIngredient";
import { fetchIngredientButtons } from "@/utils/fetchIngredientButtons";
import IngredientButton from "./IngredientButton";

export default function MealButton({ meal, isLogged, onClick, isActive , mealId}) {
    const data = { id: 1, name: "Chicken breast 100g", kcal: 165, protein: 31, carbs: 0, fat: 3.6 };
  const label = `${data.kcal} kcal • ${data.protein}P/${data.carbs}C/${data.fat}F`;
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [reloadTick, setReloadTick] = useState(0); 


      useEffect(() => {
         if (mealId == null || mealId === "") {
            setItems([]);
            setError(null);
            return;
              }
       
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
    }, [mealId, reloadTick]);
  
  
      const handleRemove = async (barcode) => {
      // optional: optimistic UI
      setItems((prev) => prev.filter((x) => x.barcode !== barcode));
      try {
        await deleteIngredient(mealId, barcode)
              setReloadTick(t => t + 1);
      } catch (e) {
      setError(e);
      setReloadTick(t => t + 1);
      }
    };
  

  return (
    <div className="w-full">
    <button
      
      onClick={onClick}
      className={`w-130 ml-10 mr-10 px-4 py-2  text-white transition duration-300 border 
        ${isActive ? 'pt-2 pb-00 bg-gray-600  hover:bg-gray-500 rounded-t-xl border-green-600  '  
          : isLogged ? 'py-2 bg-gray-600  hover:bg-gray-500 rounded-xl border-green-600' 
          : 'py-2  bg-gray-700 hover:bg-gray-500 rounded-xl  border-green-600'}
      `}
    >
      {isLogged ? `${meal} (Logged)` : meal}
    </button>
         <div
            className={`overflow-hidden transition-all duration-300 ml-10 mr-10 w-130 rounded-br-bl  bg-gray-500 rounded-b-2xl
              ${isActive ? 'min-h-30 max-h-90 opacity-100' : 'max-h-0 opacity-0  '}
            `}>

            <div className={`  text-white transition duration-300  bg-gray-500`}>
              <div>
          <IngredientSearchBar 
              isActive={isActive}
              mealId = {mealId} 
              onAdded={() => setReloadTick(t => t + 1)}/>
              {/*ingredients buttons */}
                  <div className="flex flex-col gap-2 ">
                    {items.map(it => (
                      <IngredientButton key={it.name} data={it} onRemove={()=>handleRemove(it.barcode)}/>
                    ))}
                    {items.length === 0 && <p className="text-sm text-gray-500">No ingredients.</p>}
                  </div>              
          </div>

        </div>
        </div>

  </div>
  );
  

}