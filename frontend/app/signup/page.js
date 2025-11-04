'use client';

import { useState } from 'react';
import Threads from '@/components/Threads';



export default function SignupPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSignup = async () => {
    const res = await fetch('http://localhost:8000/Signup/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });

    if (res.ok) {
      setMessage('Signup successful. You can now login.')
      ;
    } else {
      const err = await res.json();
      setMessage(`Error: ${err.detail || 'Signup failed'}`);
    }
  };

  return (
    <>
                <div
                className="fixed inset-0 -z-10 pointer-events-none"
                aria-hidden
                >
                    <div className="absolute inset-0">
                        <div style={{ width: '100%', height: '600px', position: 'relative' }}>
                        <Threads
                            amplitude={1}
                            distance={0}
                            enableMouseInteraction={true}
                        /></div>
                    </div>
            </div>
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Sign Up</h2>
      <input 
        className = "border p-2 w-full mb-2"
        placeholder = "Username"
        value={username}
         onChange={(e) => setUsername(e.target.value)}></input>
      <input
        className="border p-2 w-full mb-2"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        className="border p-2 w-full mb-2"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button
        onClick={handleSignup}
        className="bg-blue-600 text-white px-4 py-2 w-full rounded"
      >
        Sign Up
      </button>
      {message && <p className="mt-2 text-sm">{message}</p>}
    </div></>
  );
}
