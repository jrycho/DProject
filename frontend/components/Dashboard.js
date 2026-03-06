"use client";

import { useEffect, useMemo, useState } from "react";
import GraphComponent from "@/components/GraphComponent";
import { fetchTrackerData, calculateDailyMacros } from "@/utils/tracker";

function toNumber(x) {
  const n = Number(x);
  return Number.isFinite(n) ? n : 0;
}

export default function Dashboard({ date }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [goals, setGoals] = useState(null);
  const [current, setCurrent] = useState(null);
  const dateKey = date.toISOString().split("T")[0];

  useEffect(() => {
    let cancelled = false;

    async function run() {
      try {
        setLoading(true);
        setError("");

        const goalResp = await fetchTrackerData();
        const currentResp = await calculateDailyMacros(dateKey);
        console.log("HERE" ,currentResp)

        if (cancelled) return;

        // ---- Normalize shapes (adjust here if your API returns a different structure)
        const goalMacros = goalResp?.target_macros ?? goalResp; // supports both shapes
        const curMacros = currentResp;

        setGoals({
          calories: toNumber(goalMacros?.calories),
          protein: toNumber(goalMacros?.protein),
          carbs: toNumber(goalMacros?.carbs),
          fat: toNumber(goalMacros?.fat),
        });

        setCurrent({
          calories: toNumber(curMacros?.calories),
          protein: toNumber(curMacros?.protein),
          carbs: toNumber(curMacros?.carbs),
          fat: toNumber(curMacros?.fats),
        });
      } catch (e) {
        setError(e?.message || "Failed to load tracker data.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, [date]);

  if (loading) {
    return <div className="p-6 text-sm text-gray-500">Loading dashboard…</div>;
  }

  if (error) {
    return <div className="p-6 text-sm text-red-600">{error}</div>;
  }

  if (!goals || !current) {
    return <div className="p-6 text-sm text-gray-500">No tracker data.</div>;
  }

  return (
    <div className="w-full flex flex-wrap gap-8 p-6 justify-center">
      <GraphComponent
        macroType="Calories"
        current={current.calories}
        goal={goals.calories}
        color="#1EAA02"
        unit="kcal"
        size={250}
      />
      <GraphComponent
        macroType="Protein"
        current={current.protein}
        goal={goals.protein}
        color="#22c55e"
        unit="g"
        size={200}
      />
      <GraphComponent
        macroType="Carbs"
        current={current.carbs}
        goal={goals.carbs}
        color="#0055DF"
        unit="g"
        size={200}
      />
      <GraphComponent
        macroType="Fats"
        current={current.fat}
        goal={goals.fat}
        color="#C70000"
        unit="g"
        size={200}
      />
    </div>
  );
}
