import { authFetch } from './authFetch';
//TODO: API_ORIGIN
const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;;


export async function saveSettings(settings) {
    try {        
        const response = await authFetch(`${API_ORIGIN}/settings/save_settings`,
            {method : 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify(settings),
            }
        )
        if (!response.ok) throw new Error('Failed to save settings');
        const data = await response.json();
        console.log(data)


    } catch (err) {
        console.error('Failed to save settings:', err);
    }
}
    