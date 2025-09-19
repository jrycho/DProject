'use client';

import MealLogger from '@/components/MealLogger';

export default function Page() {
  return (
    <main className="p-4">
      <h1 className="text-2xl font-bold mb-4">Meal Logger</h1>
      <MealLogger />
    </main>
  );
}