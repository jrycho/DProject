import { authFetch } from "./authFetch";
import { API_ORIGIN } from "./apiConfig";
const API_BASE_URL = `http://localhost:8000`;

export async function optimizeFunction(mealId) {
    try {
        const res = await authFetch(`${API_ORIGIN}/optim/optimize/${encodeURIComponent(mealId)}`,
    {
      method: "GET",
      headers: {"Content-Type": "application/json",},
    }
  )
             


        return res.json();
    } catch (error) {
        
    }
    
}