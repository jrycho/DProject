import { authFetch } from './authFetch';

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;
//TODO: API_ORIGIN
export async function getLastSettings() {
    try {        
        const response = await authFetch(`${API_ORIGIN}/settings/get_settings`,
            {method : 'GET',
             headers: { 'Content-Type': 'application/json' },
             
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
    
