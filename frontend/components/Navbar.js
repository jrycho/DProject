"use client";

import { useState } from "react";

export default function Navbar() {
    const [open, setOpen] = useState(false);

    return(
        <>
        <header className="fixed top-0 inset-x-0 z-50 bg-gray-600 border-b border-green-600 shadow-sm">
            <div className="mx-auto flex h-14 max-w-7x1 items-center justify-between px-4">
                {/* logo */}
                <a href="/home" className="text-lg  text-white">
                    MyApp
                </a>
                        {/* Menu button  */}
        <button
          onClick={() => setOpen(true)}
          className="inline-flex items-center gap-2 rounded-md px-3 py-2 hover:bg-gray-500"
          aria-label="Open menu"
        >
          <span className="text-sm text-white">Menu</span>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
             </svg>
            </button>
            </div>
        </header>

        {open && (
            <div 
            onClick={() => setOpen(false)}
            className="fixed inset-0 u-40 bg-black/40"/>

            
        )}

      {/* Right drawer */}
      <aside
        className={`fixed right-0 top-0 z-50 h-full w-64 bg-gray-600 shadow-lg transform transition-transform ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between p-4 border-b">
          <span className="font-semibold text-white">Menu</span>
          <button onClick={() => setOpen(false)} className="p-2 hover:bg-gray-100 rounded">
            ✕
          </button>
        </div>
        <nav className="p-4 space-y-2">
          <a href="/login" className="block px-2 py-1 hover:bg-gray-500 rounded text-white">Log in</a>
          <a href="/signup" className="block px-2 py-1 hover:bg-gray-500 rounded text-white">Sign up</a>
        </nav>
      </aside>
    </>
    );
}