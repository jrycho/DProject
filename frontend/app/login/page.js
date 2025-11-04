'use client';

import {useState} from 'react';
import Navbar from '@/components/Navbar';
import { useRouter } from "next/navigation";
import Threads from '@/components/Threads';


export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const router = useRouter();
    

    const handleLogin = async() => {
        try {
        const body = new URLSearchParams();
            body.append('grant_type', 'password');
            body.append('username', email);
            body.append('password', password);

            const response = await fetch('http://localhost:8000/Auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
            body: body.toString(),
        });
         if (!response.ok) {
            const err = await response.json();

            let errorText = 'Login failed';
            if (Array.isArray(err.detail)) {
            errorText = err.detail.map((e) => e.msg).join(', ');
            } else if (typeof err.detail === 'string') {
            errorText = err.detail;
            }

            setMessage(`Error: ${errorText}`);
            return;
        }

        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        setMessage('Login successful! Redirecting...');
        router.push('/home');
        } catch (error) {
        setMessage('Login failed. Check your connection or credentials.');
        }
    };

        

    return (
        <>
        <Navbar/>
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

        <div className="p-4 max-w-md mx-auto mt-20">
            <h2 className="text-xl font-bold mb-4">Log In</h2>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="border p-2 w-full mb-2"
            />
            <input
                className = "border p-2 w-full mb-2"
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}/>
            <button 
                onClick={handleLogin}
                className="bg-blue-600 text-white px-4 py-2 w-full rounded">
                Login

            </button>
                {message && <p className="mt-2 text-sm">{message}</p>}
             </div>
             </>
    )
}