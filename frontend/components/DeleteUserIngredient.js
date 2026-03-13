"use react"
import { TrashIcon } from "@heroicons/react/24/outline";
export default ({ data, removeFunction, closeFunction }) => {
  const kcal = data.nutriments.energy_kcal_100g;
  const protein = data.nutriments.proteins_100g;
  const carbs = data.nutriments.carbohydrates_100g;
  const fat = data.nutriments.fat_100g;

  const label = `${kcal} kcal/100 g
   • ${protein} g Protein
    • ${carbs} g Carbs
     • ${fat} g Fats`;
  
  
     return (
    <>
      <div className=" w-full h-29 md:h-29 relative">
        <div
          className="bg-gray-600 border-green-600 border rounded-xl shadow-sm
               hover:bg-gray-500 active:scale-[0.98]
               focus-within:ring-2 focus-within:ring-offset-2
               flex items-center justify-between
               px-5 py-3 text-sm text-white font-sans h-full"
        >
          {/* Left side - Info */}
          <div className="flex flex-col gap-1 max-w-[50%] md:max-w-[50%]">
            <span className="truncate font-medium">{data.product_name}</span>
            <span className="text-xs text-gray-300">{label}</span>
          </div>

          {/* Close Button */}
          <button
            type="button"
            onClick={closeFunction}
            className="absolute -top-2 -right-2 bg-red-500
               w-6 h-6 rounded-full text-xs
               flex items-center justify-center
               hover:bg-red-600"
          >
            X
          </button>
          <button className="w-max-[40%] md:w-35 flex items-center gap-2 px-4 py-2 bg-red-500 text-white text-xs md:text-xm rounded-md hover:bg-red-600 transition" onClick={removeFunction}>
            <TrashIcon className="w-5 h-5"  />
            Delete ingredient
          </button>
        </div>
      </div>
    </>
  );
};
  