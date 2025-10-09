'use client';

import MealLogger from '@/components/MealLogger';
import Navbar from '@/components/Navbar';
import OptimizeButton from '@/components/OptimizeButton';
import {MealIdCtx} from '@/utils/mealIdCtx'

export default function Page() {
  return (
    <main className="p-4">

      <Navbar />
      <MealLogger />
    </main>

  );
}