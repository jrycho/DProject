import { authFetch } from './authFetch';

//TODO: fetching in backend

const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL;
/**
 * Fetch logs for a given date and update the state.
 * @param {string} dateKey - Date in YYYY-MM-DD format
 * @param {function} setLogs - React state setter for logs
 */
export async function fetchLogs(dateKey, setLogs) {
    try {        
        const response = await authFetch(`${API_ORIGIN}/logs/fetch_meal_by_date?date=${dateKey}`)
        if (!response.ok) throw new Error('Failed to fetch logs');
        const data = await response.json();

        if (Array.isArray(data) && data.length === 0) {
        console.log('No logs found for this date');
        }
  
        setLogs(Array.isArray(data) ? data : []);
        return data;
    } catch (err) {
        console.error('Failed to fetch logs:', err);
        setLogs([]); // fallback to empty list if error
        return [];
    }
}
    