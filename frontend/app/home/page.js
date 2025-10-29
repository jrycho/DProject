'use client';

import MealLogger from '@/components/MealLogger';
import Navbar from '@/components/Navbar';
import OptimizeButton from '@/components/OptimizeButton';
import {MealIdCtx} from '@/utils/mealIdCtx'
import ProtectedPage from '@/components/ProtectedPage';
import Threads from '@/components/Threads';

export default function Page() {
  return (
    
    <ProtectedPage>
      <main className="p-4">
      <Navbar />
                <div
          className="fixed inset-0 -z-10 pointer-events-none"
          aria-hidden
        >
          <div style={{ width: '100%', height: '600px', position: 'relative' }}>
          <Threads
            amplitude={1}
            distance={0}
            enableMouseInteraction={true}
  /></div></div>

      <MealLogger />
    </main>
    </ProtectedPage>

  );
}