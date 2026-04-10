import { useEffect, useRef, useState } from "react";
import { fetchMe } from "@/utils/fetchMe";
import { addShareKey } from "@/utils/addShareKey";
import { changeUsername } from "@/utils/changeUsername";
import { getSharedKeys } from "@/utils/getSharedKeys";
import { deleteSharedKey } from "@/utils/deleteSharedKey";
import Portal from "@/utils/portal";
import GuideButton from "@/components/GuideButton";

export default function SharePopup() {
  const [open, setOpen] = useState(false);
  const [manageKeysOpen, setManageKeysOpen] = useState(false);
  const [username, setUsername] = useState("");
  const [shareCode, setShareCode] = useState("");
  const [shareKey, setShareKey] = useState("");
  const [sharedKeysWithMe, setSharedKeysWithMe] = useState([]);
  const [sharedKeysLoading, setSharedKeysLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [keyError, setKeyError] = useState("");
  const [usernameError, setUsernameError] = useState("");
  const [sharedKeysError, setSharedKeysError] = useState("");
  

  const btnRef = useRef(null);
  const popRef = useRef(null);

  // fetch data when opened
  useEffect(() => {
    if (!open) return;

    (async () => {
      try {
        // change these endpoints to yours
        const r = await fetchMe();
        const d = r; // expects { username, shareCode }
        setUsername(d.username || "");
        setShareCode(d.share_key || "");
      } catch (e) {
        console.log("fetch failed", e);
      }
    })();
  }, [open]);

  useEffect(() => {
    if (!manageKeysOpen) return;

    (async () => {
      setSharedKeysLoading(true);
      setSharedKeysError("");
      try {
        const data = await getSharedKeys();
        setSharedKeysWithMe(Array.isArray(data) ? data : []);
      } catch (e) {
        setSharedKeysError("Failed to load shared keys");
        console.log("fetch shared keys failed", e);
      } finally {
        setSharedKeysLoading(false);
      }
    })();
  }, [manageKeysOpen]);

  // close on outside click + ESC
  useEffect(() => {
    if (!open) return;

    const onKey = (e) => e.key === "Escape" && setOpen(false);
    const onDown = (e) => {
      const inPopup = popRef.current && popRef.current.contains(e.target);
      const inBtn = btnRef.current && btnRef.current.contains(e.target);
      if (!inPopup && !inBtn) setOpen(false);
    };

    window.addEventListener("keydown", onKey);
    window.addEventListener("mousedown", onDown);
    return () => {
      window.removeEventListener("keydown", onKey);
      window.removeEventListener("mousedown", onDown);
    };
  }, [open]);

  async function saveUsername() {
    try {
      const res = await changeUsername(username);
      alert(res.message);
    } catch (e) {
      setUsernameError("You can change username only once every 24h");
      console.log("save username failed", e);
    }
  }

  async function handleAddShareKey() {
    try {
      await addShareKey(shareKey);
      console.log("added key", shareKey);
      setShareKey("");
      setKeyError("");
      alert("Share key added!");
    } catch (e) {
      setKeyError("Invalid key or internal error");
      console.log("add share key failed", e)
    }
  }

  async function handleDeleteSharedKey(sharedKeyToDelete) {
    try {
      await deleteSharedKey(sharedKeyToDelete);
      setSharedKeysWithMe((prev) =>
        prev.filter((item) => item.shared_key !== sharedKeyToDelete),
      );
    } catch (e) {
      setSharedKeysError("Failed to delete shared key");
      console.log("delete shared key failed", e);
    }
  }

  return (
<div>
  <button
    ref={btnRef}
    onClick={() => setOpen((v) => !v)}
    className="block w-full rounded px-2 py-1 text-left text-white hover:bg-[#035811]"
  >
    My account
  </button>

  {open && (
    <Portal>
      {/* Fullscreen backdrop */}
      <div
        className="fixed inset-0 z-[99999] flex items-center justify-center bg-black/40"
        onMouseDown={(e) => {
          // close only when clicking the backdrop (outside the modal)
          if (e.target === e.currentTarget) setOpen(false);
        }}
      >
        {/* Modal box (ALL content goes inside this box) */}
        <div
          ref={popRef}
          onMouseDown={(e) => e.stopPropagation()} // extra safety
          className="w-[360px] rounded-2xl border border-green-600 bg-gray-700 p-6 shadow-lg text-white"
        >
          <div className="mb-6 flex items-center justify-between gap-3">
            <h2 className="text-2xl font-semibold">My account</h2>
            <GuideButton guideKey="myAccountSharing" buttonText="?" />
          </div>

          <div className="mb-4">
            <div className="text-sm text-gray-300">Username</div>

            <div className="mt-2 flex gap-2">
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="h-10 flex-1 rounded-lg border border-green-600 bg-gray-800 px-3 text-sm text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />

              <button
                onClick={saveUsername}
                className="h-10 w-24 rounded-lg bg-green-600 border border-green-600 text-sm font-medium text-white hover:bg-green-500 transition"
              >
                Save
              </button>
            </div>
            <div>
              {usernameError && (
                <p className="mt-1 text-sm text-red-400">{usernameError}</p>
              )}
            </div>
          </div>

          <div className="mb-4">
            <div className="text-sm text-gray-300">Share code</div>

            <div className="mt-2 flex gap-2">
              <input
                value={shareCode}
                readOnly
                className="h-10 flex-1 rounded-lg border border-green-600 bg-gray-800 px-3 text-sm text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />

              <button
                onClick={() => {
                  navigator.clipboard.writeText(shareCode);
                  setCopied(true);
                  setTimeout(() => setCopied(false), 1500);
                }}
                className="h-10 w-24 rounded-lg bg-green-600 border border-green-600 text-sm font-medium text-white hover:bg-green-500 transition"
              >
                {copied ? "Copied!" : "Copy"}
              </button>
            </div>
          </div>

          <div>
            <div className="text-sm text-gray-300">Add share key</div>

            <div className="mt-2 flex gap-2">
              <input
                value={shareKey}
                onChange={(e) => setShareKey(e.target.value)}
                placeholder="paste key"
                className="h-10 flex-1 rounded-lg border border-green-600 bg-gray-800 px-3 text-sm text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />

              <button
                onClick={handleAddShareKey}
                className="h-10 w-24 rounded-lg bg-green-600 border border-green-600 text-sm font-medium text-white hover:bg-green-500 transition"
              >
                Add
              </button>
            </div>

            <div>
              {keyError && (
                <p className="mt-1 text-sm text-red-400">{keyError}</p>
              )}
            </div>
          </div>

          <div className="mt-4">
            <button
              onClick={() => setManageKeysOpen(true)}
              className="w-full rounded-lg border border-green-600 bg-gray-800 px-3 py-2 text-sm font-medium text-white transition hover:bg-gray-600"
            >
              Manage keys shared with me
            </button>
          </div>
        </div>
      </div>
    </Portal>
  )}

  {manageKeysOpen && (
    <Portal>
      <div
        className="fixed inset-0 z-[99999] flex items-center justify-center bg-black/40"
        onMouseDown={(e) => {
          if (e.target === e.currentTarget) setManageKeysOpen(false);
        }}
      >
        <div
          onMouseDown={(e) => e.stopPropagation()}
          className="w-[420px] max-w-[calc(100vw-2rem)] rounded-2xl border border-green-600 bg-gray-700 p-6 shadow-lg text-white"
        >
          <div className="mb-4 flex items-center justify-between gap-3">
            <h2 className="text-xl font-semibold">Keys shared with me</h2>
            <button
              onClick={() => setManageKeysOpen(false)}
              className="rounded px-2 py-1 text-sm text-white transition hover:bg-gray-600"
            >
              Close
            </button>
          </div>

          <div className="max-h-[18rem] overflow-y-auto custom-scrollbar space-y-3 pr-1">
            {sharedKeysLoading && (
              <p className="text-sm text-gray-300">Loading...</p>
            )}

            {!sharedKeysLoading && sharedKeysWithMe.length === 0 && !sharedKeysError && (
              <p className="text-sm text-gray-300">No shared keys added.</p>
            )}

            {!sharedKeysLoading &&
              sharedKeysWithMe.map((item) => (
                <div
                  key={item.shared_key}
                  className="rounded-lg border border-green-600 bg-gray-800 px-3 py-3"
                >
                  <div className="text-sm font-medium text-white">{item.username}</div>
                  <div className="mt-1 break-all text-xs text-gray-300">
                    {item.shared_key}
                  </div>
                  <button
                    onClick={() => handleDeleteSharedKey(item.shared_key)}
                    className="mt-3 rounded-lg bg-red-600 px-3 py-1 text-sm text-white transition hover:bg-red-500"
                  >
                    Delete key
                  </button>
                </div>
              ))}

            {sharedKeysError && (
              <p className="text-sm text-red-400">{sharedKeysError}</p>
            )}
          </div>
        </div>
      </div>
    </Portal>
  )}
</div>

  );
}
