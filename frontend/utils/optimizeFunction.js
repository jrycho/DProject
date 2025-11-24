import { authFetch } from "./authFetch";
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;;

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