import { authFetch } from './authFetch';

const API_BASE_URL = `http://localhost:8000`;

export async function getLastSettings() {
    try {        
        const response = await authFetch(API_BASE_URL+`/settings/get_settings`,
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
    
