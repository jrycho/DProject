import { authFetch } from './authFetch';

const API_BASE_URL = `http://localhost:8000`;


export async function saveSettings(settings) {
    try {        
        const response = await authFetch(API_BASE_URL+`/settings/save_settings`,
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
    