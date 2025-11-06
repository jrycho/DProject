'use client'
import MagicBento from '@/components/MagicBento'
import MealButton from '@/components/MealButton';
import { useState, useEffect , createContext, useContext, useCallback} from 'react';
import { logMeal, getLogsByDate } from '@/utils/log_meal';
import SettingsComponent from '@/components/SettingsComponent';
import { fetchLogs} from "@/utils/fetchLogs"
import { getLastSettings } from '@/utils/getLastSettings';
import Threads from '@/components/Threads'
import React from 'react';
import DateSelector from '@/components/DayNavigation';





const MEAL_TYPES = ['Breakfast', 'Snack 1', 'Lunch', 'Snack 2', 'Dinner', 'Snack 3'];
export default function testPage() {
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [logs, setLogs] = useState([]);
    const [activeMealLog, setActiveMealLog] = useState(false);
    const [activeMealId, setActiveMealId] = useState(null);

    const [settingsObj, setSettingsObj] = useState(null); 
    const [LastSettings, setLastSettings] = useState(null);
    const [ready, setReady] = useState(false)


    const dateKey = selectedDate.toISOString().split('T')[0]


    const handleChangeDay = useCallback(({selectedDate }) => {
      setSelectedDate(selectedDate)
      console.log("THE DATE IS NOW: "+selectedDate)
  }, []);

    useEffect(() => {


        fetchLogs(dateKey, setLogs);}, [dateKey]);
        console.log(logs);




    //function if not logged, log, if logged, find and set to active
    async function mealButtonClick(mealType, isLogged) {
    
    if (activeMealLog?.type_of_meal === mealType) {
    setActiveMealLog(null);
    setActiveMealId(null);
    return;
    }
   
    if (!isLogged) {
    const newLog = await  logMeal(mealType, dateKey);

    setLogs(prev => [...prev, newLog]);
    

    await fetchLogs(dateKey, setLogs);
    

    setActiveMealLog(newLog);
    setActiveMealId(newLog.meal_id);
    

    } else { 
        const existingLog = logs.find(log => log.date === dateKey && log.type_of_meal === mealType);
        setActiveMealLog(existingLog);
        setActiveMealId(existingLog.meal_id);
        console.log('active meal log:' +  activeMealLog?.meal_id ?? '(none)');
    }
    }

return(
  <>
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
<DateSelector
  onClickDays={handleChangeDay}/>
<MagicBento 
  textAutoHide={true}
  enableStars={true}
  enableSpotlight={true}
  enableBorderGlow={true}
  enableTilt={true}
  enableMagnetism={true}
  clickEffect={true}
  spotlightRadius={3}
  particleCount={12}
  glowColor="0, 255, 136"
>
        <div className="card-grid"
          style={{
    width: 'min(1200px, 95vw)',
    height: '2000px',
    margin: '0 auto',
    display: 'grid',
    gap: '0.5em',
    padding: '0.75em',
    gridTemplateColumns: 'repeat(4, minmax(0, 1fr))', // 4 tracks to span across
    gridAutoRows: '200px', // base row height so row spans have meaning
  }}>
        <div className="magic-bento-card magic-bento-card--border-glow">
          <div className="magic-bento-card__header">
            <h3 className="magic-bento-card__title">Meals</h3>
          </div>
          <div className="magic-bento-card__content" style={{ overflow: 'auto' }}>
            <div className="flex flex-col gap-2">
                  {MEAL_TYPES.map(mealType => {
                      const log = logs.find(log => log.type_of_meal === mealType);
                        const isActive = activeMealLog && log?.meal_id && activeMealLog.meal_id === log.meal_id;
                      return (
                          <MealButton
                              key={mealType}
                              meal={mealType}
                              mealId = {activeMealId}
                              isLogged={!!log}
                              isActive={  activeMealLog  != null && log?.meal_id != null && activeMealLog.meal_id === log.meal_id}
                              onClick={() => mealButtonClick(mealType, !!log)}
                          />
                      );
                  })}            
            </div>
          </div>
        </div>
              </div>
  </MagicBento></>
);
}