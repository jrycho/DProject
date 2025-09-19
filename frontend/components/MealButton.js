import { useEffect } from "react";

export default function MealButton({ meal, isLogged, onClick, isActive }) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded text-white transition 
        ${isActive ? 'bg-yellow-500' : isLogged ? 'bg-green-500' : 'bg-blue-500 hover:bg-blue-600'}
      `}
    >
      {isLogged ? `${meal} (Logged)` : meal}
    </button>
  );
}