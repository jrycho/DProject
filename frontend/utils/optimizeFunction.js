import { authFetch } from "./authFetch";

const API_BASE_URL = `http://localhost:8000`;

export async function optimizeFunction(mealId) {
    try {
        const res = await authFetch(API_BASE_URL+`/optim/optimize/${encodeURIComponent(mealId)}`,
            {method : 'GET',
             headers: { 'Content-Type': 'application/json' },
             
            }
        )
        console.log(res)
    } catch (error) {
        
    }
    
}