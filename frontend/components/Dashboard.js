"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import GraphComponent from "@/components/GraphComponent";
import { fetchTrackerData, calculateDailyMacros } from "@/utils/tracker";
import GuideButton from "@/components/GuideButton";

const EMPTY_MACROS = {
  calories: 0,
  protein: 0,
  carbs: 0,
  fat: 0,
};

function toNumber(x) {
  const n = Number(x);
  return Number.isFinite(n) ? n : 0;
}

export default function Dashboard({ date, refresh }) {
  const router = useRouter();
  const [goals, setGoals] = useState(EMPTY_MACROS);
  const [current, setCurrent] = useState(EMPTY_MACROS);
  const dateKey = date.toISOString().split("T")[0];

  useEffect(() => {
    let cancelled = false;

    async function run() {
      try {
        const goalResp = await fetchTrackerData(dateKey);
        const currentResp = await calculateDailyMacros(dateKey);

        if (cancelled) return;

        const goalMacros = goalResp?.target_macros ?? goalResp;
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
        if (!cancelled && e?.message?.includes("Failed to fetch tracker data: 400")) {
          router.push("/set_up_my_account");
          return;
        }
        console.error("Failed to load tracker data.", e);
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, [dateKey, refresh, router]);

  return (
    <div className="relative w-full">
      <div className="absolute top-0 right-0 z-10">
        <GuideButton guideKey="trackerGoals" buttonText="?" />
      </div>

      <div className="w-full flex flex-wrap gap-8 p-6 justify-center">
        <GraphComponent
          macroType="Calories"
          current={current.calories}
          goal={goals.calories}
          color="#1EAA02"
          unit="kcal"
          mobileSize={140}
          size={260}
        />
        <GraphComponent
          macroType="Protein"
          current={current.protein}
          goal={goals.protein}
          color="#22c55e"
          unit="g"
          mobileSize={120}
          size={220}
        />
        <GraphComponent
          macroType="Carbs"
          current={current.carbs}
          goal={goals.carbs}
          color="#0055DF"
          unit="g"
          mobileSize={120}
          size={220}
        />
        <GraphComponent
          macroType="Fats"
          current={current.fat}
          goal={goals.fat}
          color="#C70000"
          unit="g"
          mobileSize={120}
          size={220}
        />
      </div>
    </div>
  );
}
