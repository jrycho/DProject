'use client';

import MealLogger from '@/components/MealLogger';
import Navbar from '@/components/Navbar';
import OptimizeButton from '@/components/OptimizeButton';
import {MealIdCtx} from '@/utils/mealIdCtx'
import ProtectedPage from '@/components/ProtectedPage';

export default function Page() {
  return (
    <ProtectedPage>
      <main className="p-4">
      <Navbar />
      <MealLogger />
    </main>
    </ProtectedPage>

  );
}