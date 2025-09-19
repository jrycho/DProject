// TODO: addable logout helper

//define function
//Args: 
//  -url: str
//  -options: obj

// authFetch.js

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function authFetch(path, options = {}) {
  const token = localStorage.getItem('token');
  if (!token) throw new Error('No access token found');

  const url = path.startsWith('http') ? path : `${API_BASE_URL}${path}`;
  const headers = { ...options.headers, Authorization: `Bearer ${token}` };

  const response = await fetch(url, { ...options, headers, mode: 'cors' });

  // optional: auto-logout on 401
  if (response.status === 401) {
    localStorage.removeItem('token');
    // window.location.href = '/login'; // uncomment if you want redirect
  }

  return response; // returns a Response object
}