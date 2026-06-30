
import { useState, useEffect, useRef } from 'react';
import { useCoherenceStore } from '../store/coherenceStore';

export interface BiometricHistory {
  pulse: number[]; // FPS
  pressure: number[]; // Cognitive Load
  temp: number[]; // Inverted Coherence (Entropy)
}

const HISTORY_LENGTH = 30; // Number of data points to keep

export const useSystemMetrics = () => {
  const [history, setHistory] = useState<BiometricHistory>({
    pulse: Array.from({ length: HISTORY_LENGTH }, () => 60),
    pressure: Array.from({ length: HISTORY_LENGTH }, () => 0.2),
    temp: Array.from({ length: HISTORY_LENGTH }, () => 0.1),
  });

  const frameCountRef = useRef(0);
  const lastFrameTimeRef = useRef(0);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    lastFrameTimeRef.current = performance.now();
    // 1. FPS Tracker
    const trackFrame = () => {
      frameCountRef.current++;
      requestAnimationFrame(trackFrame);
    };
    const animationId = requestAnimationFrame(trackFrame);

    // 2. Metrics Snapshot Loop (every 1000ms)
    intervalRef.current = window.setInterval(() => {
      const now = performance.now();
      const elapsed = now - lastFrameTimeRef.current;
      const fps = Math.round((frameCountRef.current / elapsed) * 1000);
      
      // Reset frame counters
      frameCountRef.current = 0;
      lastFrameTimeRef.current = now;

      // Get current store values
      const state = useCoherenceStore.getState();
      const load = state.cognitiveLoad;
      // Temperature is the inverse of coherence (Entropy)
      // If Coherence is 1.0, Temp is 0. If Coherence is 0.4, Temp is 0.6.
      const temperature = Math.max(0, 1 - state.coherenceIndex);

      setHistory(prev => {
        const newPulse = [...prev.pulse.slice(1), fps];
        const newPressure = [...prev.pressure.slice(1), load];
        const newTemp = [...prev.temp.slice(1), temperature];
        return { pulse: newPulse, pressure: newPressure, temp: newTemp };
      });

    }, 1000);

    return () => {
      cancelAnimationFrame(animationId);
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  return history;
};
