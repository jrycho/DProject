import { useEffect, useState } from "react";
import IngredientSearchBar from '@/components/IngredientSearchBar';

export default function MealButton({ meal, isLogged, onClick, isActive , mealId}) {


  return (
    <div className="w-full">
    <button
      
      onClick={onClick}
      className={`w-150 ml-10 mr-10 px-4 py-2  text-white transition duration-300
        ${isActive ? 'pt-2 pb-00 bg-yellow-500 rounded-tr-tl'  
          : isLogged ? 'py-2 bg-green-500 rounded' 
          : 'py-2  bg-blue-500 hover:bg-blue-600 rounded'}
      `}
    >
      {isLogged ? `${meal} (Logged)` : meal}
    </button>
         <div
        className={`overflow-hidden transition-all duration-300 ml-10 mr-10 w-150 rounded-br-bl  bg-yellow-500 rounded-b-2xl
          ${isActive ? 'min-h-30 max-h-90 opacity-100' : 'max-h-0 opacity-0  '}
        `}>
        <div className={`  text-white transition duration-300  bg-yellow-500`}>
          <div>
          <IngredientSearchBar 
              isActive={isActive}
              mealId = {mealId} />
          </div>

        </div>
        </div>

  </div>
  );
  

}