"use client";

import { useState } from "react";
import SharePopup from "./UserPopup";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const router = useRouter();

  const handleLogout = () => {
    console.log("logout");
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <>
      <header className="w-full fixed top-0 inset-x-0 z-[95] bg-[#001303] border-b border-green-600 shadow-sm">
        <div className="mx-auto flex h-25 max-w-full items-center justify-between px-4">
          {/* logo */}
          <a href="/home" className="text-lg  text-white">
            Nomingomi
          </a>
          {/* Menu button  */}
          <button
            onClick={() => setOpen(true)}
            className="inline-flex items-center gap-2 rounded-md px-0 py-2 hover:bg-[#035811]"
            aria-label="Open menu"
          >
            <span className="text-sm text-white">Menu</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </header>

      {open && (
        <div
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-40 bg-black/40"
        />
      )}

      {/* Right drawer */}
      <aside
        className={`fixed right-0 top-0 z-[100] h-full w-64 bg-[#012006] shadow-lg transform transition-transform ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between p-4 border-b">
          <span className="font-semibold text-white">Menu</span>
          <button
            onClick={() => setOpen(false)}
            className="p-2 hover:bg-[#035811] rounded"
          >
            ✕
          </button>
        </div>
        <nav className="p-4 space-y-2">
          <a
            href="/signup"
            className="block px-2 py-1 hover:bg-[#035811] rounded text-white"
          >
            Sign up
          </a>
          <a
            href="/login"
            className="block px-2 py-1 hover:bg-[#035811] rounded text-white"
          >
            Log in
          </a>
          <div>
            <button
              onClick={handleLogout}
              className="block px-2 py-1 hover:bg-[#035811] rounded text-white w-full text-left"
            >
              Log out
            </button>
            <a
              href="/home"
              className="block px-2 py-1 hover:bg-[#035811] rounded text-white"
            >
              Home
            </a>
          </div>
          <div className="items-center justify-between border-t ">
            <SharePopup className="mt-1.5" />
            <a
              href="/set_up_my_account"
              className="block px-2 py-1 hover:bg-[#035811] rounded text-white"
            >
              Set up my goals
            </a>
            <a
              href="/add_ingredients"
              className="block px-2 py-1 hover:bg-[#035811] rounded text-white"
            >
              Add my ingredients
            </a>
            <a
              href="/manage_my_ingredients"
              className="block px-2 py-1 hover:bg-[#035811] rounded text-white"
            >
              Delete my ingredients
            </a>
          </div>
        </nav>
      </aside>
    </>
  );
}
