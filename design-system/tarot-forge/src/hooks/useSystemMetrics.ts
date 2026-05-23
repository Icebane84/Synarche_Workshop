import { useEffect, useRef, useState } from "react";
import { useSharedConsciousness } from "../store/sharedConsciousness";

export type BiometricHistory = {
  pulse: number[]; // FPS
  pressure: number[]; // Cognitive Load (mapped from dissonance?)
  temp: number[]; // Inverted Coherence (Entropy)
};

const HISTORY_LENGTH = 30; // Number of data points to keep

export const useSystemMetrics = () => {
  const [history, setHistory] = useState<BiometricHistory>({
    pulse: new Array(HISTORY_LENGTH).fill(60),
    pressure: new Array(HISTORY_LENGTH).fill(0.2),
    temp: new Array(HISTORY_LENGTH).fill(0.1),
  });

  const frameCountRef = useRef(0);
  const lastFrameTimeRef = useRef(performance.now());
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
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
      const state = useSharedConsciousness.getState();

      // Map Dissonance (0-100) to Pressure (0.0-1.0)
      const load = (state.stats.dissonance || 0) / 100;

      // Map Resonance (0-100) to Temperature (inverted)
      // Resonance 100 -> Temp 0. Resonance 0 -> Temp 1.
      const resonance = state.stats.resonance || 0;
      const temperature = Math.max(0, 1 - resonance / 100);

      setHistory((prev) => {
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
