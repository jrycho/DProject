"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import { useRouter } from "next/navigation";
import ThreadsBackground from "@/components/ThreadsBackground";
import { estimateUserMacros, setUserGoals } from "@/utils/tracker";



export default function TrackerQuestioner() {
  const router = useRouter();

  // --- mode
  const [mode, setMode] = useState("estimate");

  // --- estimate form state
  const [sex, setSex] = useState("male");
  const [weight, setWeight] = useState(""); // kg
  const [height, setHeight] = useState(""); // cm
  const [age, setAge] = useState(""); // years
  const [activityLevel, setActivityLevel] = useState("moderately_active");
  const [goal, setGoal] = useState("maintain");

  // --- custom form state
  const [calories, setCalories] = useState("");
  const [protein, setProtein] = useState("");
  const [carbs, setCarbs] = useState("");
  const [fat, setFat] = useState("");

  // --- ui state
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // optional: protect route
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) router.push("/login");
  }, [router]);

  const requireTokenOrRedirect = () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setMessage("You are not logged in.");
      router.push("/login");
      return null;
    }
    return token;
  };

  const handleSubmitEstimate = async () => {
    setMessage("");
    setLoading(true);
    try {
      const token = requireTokenOrRedirect();
      if (!token) return;

      const w = Number(weight);
      const h = Number(height);
      const a = Number(age);

      if (!w || w <= 0) return setMessage("Please enter a valid weight (kg).");
      if (!h || h <= 0) return setMessage("Please enter a valid height (cm).");
      if (!a || a <= 0) return setMessage("Please enter a valid age.");

      const payload = {
        sex,
        weight: w,
        height: h,
        age: a,
        activity_level: activityLevel,
        goal,
      };

      await estimateUserMacros(payload);

      setMessage("Goals saved! Redirecting to homepage...");
      router.push("/home");
    } catch (err) {
      setMessage(err?.message || "Failed to save goals.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitCustom = async () => {
    setMessage("");
    setLoading(true);
    try {
      const token = requireTokenOrRedirect();
      if (!token) return;

      const cals = Number(calories);
      const p = Number(protein);
      const c = Number(carbs);
      const f = Number(fat);

      if (!cals || cals <= 0) return setMessage("Please enter valid calories.");
      if (p < 0 || !Number.isFinite(p)) return setMessage("Please enter valid protein (g).");
      if (c < 0 || !Number.isFinite(c)) return setMessage("Please enter valid carbs (g).");
      if (f < 0 || !Number.isFinite(f)) return setMessage("Please enter valid fat (g).");

      // Adjust keys to match your backend contract
      const customPayload = {
        calories: cals,
        protein: p,
        carbs: c,
        fat: f,
      };

      await setUserGoals(customPayload);

      setMessage("Custom goals saved! Redirecting to homepage...");
      router.push("/home");
    } catch (err) {
      setMessage(err?.message || "Failed to save goals.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (loading) return;
    if (mode === "estimate") return handleSubmitEstimate();
    return handleSubmitCustom();
  };


  return (
  <>
    <Navbar />

    <div className="fixed inset-0 -z-10 pointer-events-none" aria-hidden>
      <div className="absolute inset-0">
        <div style={{ width: "100%", height: "600px", position: "relative" }}>
          <ThreadsBackground
            amplitude={1}
            distance={0}
            enableMouseInteraction={true}
          />
        </div>
      </div>
    </div>

    <div className="max-w-md mx-auto mt-24 p-6 bg-gray-700 border border-green-600 rounded-2xl shadow-lg text-white">

      <h2 className="text-2xl font-semibold mb-6 text-center">
        Set your daily goals
      </h2>

      {/* Mode Switch */}
      <div className="flex gap-2 mb-6">
        <button
          type="button"
          onClick={() => {
            setMode("estimate");
            setMessage("");
          }}
          className={`w-full px-4 py-2 rounded-lg border transition
            ${
              mode === "estimate"
                ? "bg-green-600 border-green-600"
                : "bg-gray-600 hover:bg-gray-500 border-green-600"
            }`}
          disabled={loading}
        >
          Smart estimate
        </button>

        <button
          type="button"
          onClick={() => {
            setMode("custom");
            setMessage("");
          }}
          className={`w-full px-4 py-2 rounded-lg border transition
            ${
              mode === "custom"
                ? "bg-green-600 border-green-600"
                : "bg-gray-600 hover:bg-gray-500 border-green-600"
            }`}
          disabled={loading}
        >
          Custom goals
        </button>
      </div>

      {/* ESTIMATE FORM */}
      {mode === "estimate" && (
        <>
          <label className="text-sm text-gray-300">Sex</label>
          <select
            value={sex}
            onChange={(e) => setSex(e.target.value)}
            className="w-full p-2 mb-3 bg-gray-800 border border-green-600 rounded-lg"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>

          <label className="text-sm text-gray-300">Weight (kg)</label>
          <input
            type="number"
            placeholder="e.g. 78"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            className="w-full p-2 mb-3 bg-gray-800 border border-green-600 rounded-lg"
          />

          <label className="text-sm text-gray-300">Height (cm)</label>
          <input
            type="number"
            placeholder="e.g. 180"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
            className="w-full p-2 mb-3 bg-gray-800 border border-green-600 rounded-lg"
          />

          <label className="text-sm text-gray-300">Age</label>
          <input
            type="number"
            placeholder="e.g. 24"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            className="w-full p-2 mb-3 bg-gray-800 border border-green-600 rounded-lg"
          />

          <label className="text-sm text-gray-300">Activity level</label>
          <select
            value={activityLevel}
            onChange={(e) => setActivityLevel(e.target.value)}
            className="w-full p-2 mb-3 bg-gray-800 border border-green-600 rounded-lg"
          >
            <option value="sedentary">Sedentary</option>
            <option value="lightly_active">Lightly active</option>
            <option value="moderately_active">Moderately active</option>
            <option value="very_active">Very active</option>
            <option value="athlete">Athlete</option>
          </select>

          <label className="text-sm text-gray-300">Goal</label>
          <select
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            className="w-full p-2 mb-4 bg-gray-800 border border-green-600 rounded-lg"
          >
            <option value="weight_loss">Weight loss</option>
            <option value="maintain">Maintain</option>
            <option value="weight_gain">Weight gain</option>
          </select>

          
        </>
      )}

      {/* CUSTOM FORM */}
      {mode === "custom" && (
        <>
          <label className="text-sm text-gray-300">Calories (kcal)</label>
          <input
            type="number"
            placeholder="e.g. 2400"
            value={calories}
            onChange={(e) => setCalories(e.target.value)}
            className="w-full p-2 mb-3 bg-gray-800 border border-green-600 rounded-lg"
          />

          <label className="text-sm text-gray-300">Protein (g)</label>
          <input
            type="number"
            placeholder="e.g. 160"
            value={protein}
            onChange={(e) => setProtein(e.target.value)}
            className="w-full p-2 mb-3 bg-gray-800 border border-green-600 rounded-lg"
          />

          <label className="text-sm text-gray-300">Carbs (g)</label>
          <input
            type="number"
            placeholder="e.g. 250"
            value={carbs}
            onChange={(e) => setCarbs(e.target.value)}
            className="w-full p-2 mb-3 bg-gray-800 border border-green-600 rounded-lg"
          />

          <label className="text-sm text-gray-300">Fat (g)</label>
          <input
            type="number"
            placeholder="e.g. 70"
            value={fat}
            onChange={(e) => setFat(e.target.value)}
            className="w-full p-2 mb-4 bg-gray-800 border border-green-600 rounded-lg"
          />


        </>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="bg-green-600 hover:bg-green-500 disabled:opacity-50 text-white px-4 py-2 w-full rounded-lg mt-6 transition"
      >
        {loading ? "Saving..." : "Save goals"}
      </button>

      {message && (
        <p className="mt-4 text-sm text-gray-300 text-center">{message}</p>
      )}
    </div>
  </>
);
}