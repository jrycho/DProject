"use client";

import { ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

export default function GraphComponent({
  macroType,
  current,
  goal,
  color = "#3b82f6",
  unit = "",
  size = 400,
}) {
  const safeCurrent = Math.max(0, current || 0);
  const safeGoal = Math.max(1, goal || 1);

  const progress = Math.min(safeCurrent, safeGoal);
  const remaining = Math.max(safeGoal - safeCurrent, 0);

  const data = [
    { name: "current", value: progress },
    { name: "remaining", value: remaining },
  ];

  return (
    <div style={{ width: size, height: size }} className="relative">
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            innerRadius="65%"
            outerRadius="90%"
            startAngle={90}
            endAngle={-270}
            stroke="none"
          >
            <Cell fill={color} />
            <Cell fill="#e5e7eb" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>

      {/* center text */}
      <div className="mt-2 absolute inset-0 flex flex-col items-center justify-center text-center">
        <div className="text-xm font-bold text-gray-200">{macroType}</div>
        <div className="text-lg font-semibold">
          {safeCurrent}/{safeGoal}
        </div>
        <div className="text-xm font-bold text-gray-200">{unit}</div>
      </div>
    </div>
  );
}
