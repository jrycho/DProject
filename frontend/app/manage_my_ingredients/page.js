// app/ingredients/add-macros/page.jsx
"use client";

import { useState } from "react";
import ProtectedPage from "@/components/ProtectedPage";
import Threads from "@/components/Threads";
import Navbar from "@/components/Navbar";
import ThreadsBackground from "@/components/ThreadsBackground";
import UserIngredientSearchbarComponent from "@/components/UserIngredientSearchbar";
import DeleteUserIngredient from "@/components/DeleteUserIngredient";
import { userIngredientDelete } from "@/utils/userIngredientDelete";

export default function ManageMyIngredients() {
    const [data, setData] = useState({});
    const [active, setActive] = useState(false);
    const [resetKey, setResetKey] = useState(0);
    
    

    function updateData(item) {
        setData(item);
        console.log("SELECTED ITEM: ", item);
        setActive(true);
    }
    
    async function onAdded(placeholder, placeholder2) {
        console.log("Delete querry");
        setResetKey((k) => k + 1);
    }
    
    async function handleDelete(barcode) {
        console.log("handle delete");
        const res = await userIngredientDelete(barcode);
        console.log(res);
    if(res) {
            console.log("Delete success");
            setActive(false);
            setData({});
        } else {
            console.log("Delete failed");
        }
    }

    function handleClose() {
        setActive(false);
        setData({});
    }


    return (
    <ProtectedPage>
      <main className="relative min-h-screen p-4">
        <Navbar />
        <ThreadsBackground />
      <div className="pt-14">
        {/* Content card (same styling as your temp-log page) */}
        <div className="w-full md:max-w-[520px] mx-auto p-6 bg-gray-700 backdrop-blur rounded-lg shadow ">
          <h1 className="text-2xl font-semibold mb-4 text-white">
            Manage my ingredients
          </h1>

          {/* Search */}
          <div className="mb-4">
            <UserIngredientSearchbarComponent
              isActive={true}
              key={resetKey}
              onSelected={updateData}
              addIngredientFunction={onAdded}
            />
          </div>

          {/* Delete panel */}
          <div>
            {active ? (
              <DeleteUserIngredient
                data={data}
                setData={setData}
                removeFunction={() => handleDelete(data.code)} // change to data.barcode if needed
                closeFunction={handleClose}
              />
            ) : (
              <p className="text-sm text-gray-200">
                Select an ingredient to delete.
              </p>
            )}
          </div>
        </div></div>
      </main>
    </ProtectedPage>
  );
}