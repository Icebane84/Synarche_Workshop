import { useEffect, useRef } from 'react';
import { useCoherenceStore } from '../store/coherenceStore';
import { executeRemCycle } from '../services';

const IDLE_THRESHOLD_MS = 60 * 1000; // 60 seconds
const REM_CYCLE_INTERVAL_MS = 5000; // Dream event every 5 seconds

export const useDreamCycle = () => {
  const setDreaming = useCoherenceStore((state) => state.setDreaming);
  const isDreaming = useCoherenceStore((state) => state.isDreaming);
  
  const idleTimerRef = useRef<number | null>(null);
  const dreamIntervalRef = useRef<number | null>(null);

  const goDeepSleep = () => {
    setDreaming(true);
  };

  const wakeUp = () => {
    if (useCoherenceStore.getState().isDreaming) {
        setDreaming(false);
    }
    resetIdleTimer();
  };

  const resetIdleTimer = () => {
    if (idleTimerRef.current) window.clearTimeout(idleTimerRef.current);
    idleTimerRef.current = window.setTimeout(goDeepSleep, IDLE_THRESHOLD_MS);
  };

  // Activity Listeners
  useEffect(() => {
    const events = ['mousemove', 'keydown', 'mousedown', 'touchstart', 'scroll'];
    const handleActivity = () => { wakeUp(); };

    events.forEach(event => { window.addEventListener(event, handleActivity); });
    resetIdleTimer(); // Init timer

    return () => {
      events.forEach(event => { window.removeEventListener(event, handleActivity); });
      if (idleTimerRef.current) window.clearTimeout(idleTimerRef.current);
    };
  }, []);

  // Dream Logic Loop
  useEffect(() => {
    if (isDreaming) {
        // Start REM Cycle Loop
        // We use setInterval to trigger the attempt, but we wrap the actual
        // execution in requestIdleCallback to ensure we are respecting the
        // "Background Processing" philosophy.
        dreamIntervalRef.current = window.setInterval(() => {
             if ('requestIdleCallback' in window) {
                 window.requestIdleCallback((deadline) => {
                     // Only execute if we have time remaining or if the OS strictly timed us out
                     if (deadline.timeRemaining() > 0 || deadline.didTimeout) {
                         executeRemCycle();
                     }
                 }, { timeout: 1000 });
             } else {
                 // Fallback for environments without requestIdleCallback
                 executeRemCycle();
             }
        }, REM_CYCLE_INTERVAL_MS);
    } else {
        if (dreamIntervalRef.current) window.clearInterval(dreamIntervalRef.current);
    }

    return () => {
        if (dreamIntervalRef.current) window.clearInterval(dreamIntervalRef.current);
    };
  }, [isDreaming]);
};