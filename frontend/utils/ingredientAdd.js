import React from 'react'
import { authFetch } from './authFetch';
import { API_ORIGIN } from '@/utils/apiConfig';

const API_BASE_URL = `http://localhost:8000`;

export async function addIngredient(barcode, mealId) {
    

        try {
            console.log(API_ORIGIN+`/logs/add_ingredient${encodeURIComponent(barcode)}?meal_id=${encodeURIComponent(mealId)}`)
            const res = await authFetch(`http://localhost:8000/logs/add_ingredient${encodeURIComponent(barcode)}?meal_id=${encodeURIComponent(mealId)}`,
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
