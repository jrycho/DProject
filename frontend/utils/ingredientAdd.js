import React from 'react'
import { authFetch } from './authFetch';

//TODO: API_ORIGIN
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;

export async function addIngredient(barcode, mealId) {
    

        try {
            console.log(API_ORIGIN+`/logs/add_ingredient${encodeURIComponent(barcode)}?meal_id=${encodeURIComponent(mealId)}`)
            const res = await authFetch(`${API_ORIGIN}/logs/add_ingredient/${encodeURIComponent(barcode)}?meal_id=${encodeURIComponent(mealId)}`,
                {method : 'POST',
                headers: { 'Content-Type': 'application/json' },
            }
            )
            if (!res.ok) {
                throw new Error(`Failed to add ingredient: ${res.status}`);
            }   
        } catch (error) {
            
        }
   
}
