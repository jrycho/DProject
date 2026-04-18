// TODO: addable logout helper

//define function
//Args: 
//  -url: str
//  -options: obj

// authFetch.js

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || "/api").replace(/\/$/, "");

export async function authFetch(path, options = {}) {
  const token = localStorage.getItem('token');
  if (!token) throw new Error('No access token found');

  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  const url = path.startsWith('http') || normalizedPath === API_BASE_URL || normalizedPath.startsWith(`${API_BASE_URL}/`)
    ? path
    : `${API_BASE_URL}${normalizedPath}`;
  const headers = { ...options.headers, Authorization: `Bearer ${token}` };

  const response = await fetch(url, { ...options, headers });

  // optional: auto-logout on 401
  if (response.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
  }

  return response; // returns a Response object
}
