import { authFetch } from './authFetch';

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function getLastSettings(meal_type) {
        const payload = { meal_type: meal_type};
        console.log(payload);
    try {        
        const response = await authFetch(`${API_ORIGIN}/settings/items`,
            {method : 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify(payload)
             
            }
        )
        if (!response.ok) throw new Error('Failed to get settings');
        const data = await response.json();
        console.log(data)
        return (data)


    } catch (err) {
        console.error('Failed to get settings:', err);
    }
}
    
 
