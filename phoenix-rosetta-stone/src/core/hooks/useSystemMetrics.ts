import { useState, useEffect, useRef } from "react";
import { useCognitiveCore } from "@state/useCognitiveCore";

export interface BiometricHistory {
  pulse: number[]; // FPS
  pressure: number[]; // Cognitive Load / Activity
  temp: number[]; // Entropy (Inverse of coherence)
}

const HISTORY_LENGTH = 15; // Compact history for mini sparklines

export const useSystemMetrics = () => {
  const [history, setHistory] = useState<BiometricHistory>({
    pulse: Array.from({ length: HISTORY_LENGTH }, () => 60),
    pressure: Array.from({ length: HISTORY_LENGTH }, () => 0.15),
    temp: Array.from({ length: HISTORY_LENGTH }, () => 0.0),
  });

  const frameCountRef = useRef(0);
  const lastFrameTimeRef = useRef(performance.now());
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    // 1. FPS Tracker
    const trackFrame = () => {
      frameCountRef.current++;
      animationId = requestAnimationFrame(trackFrame);
    };
    let animationId = requestAnimationFrame(trackFrame);

    // 2. Snapshots every 1 second
    intervalRef.current = window.setInterval(() => {
      const now = performance.now();
      const elapsed = now - lastFrameTimeRef.current;
      const fps = Math.round((frameCountRef.current / elapsed) * 1000);

      // Reset
      frameCountRef.current = 0;
      lastFrameTimeRef.current = now;

      // Extract values from Cognitive Core
      const cognitiveState = useCognitiveCore.getState();
      const isProcessing = cognitiveState.isLoading;
      const coherence = cognitiveState.coherenceIndex;

      // Simulate cognitive pressure (high during load, default low/medium fluctuations)
      const simulatedPressure = isProcessing 
        ? 0.75 + Math.random() * 0.15 
        : 0.12 + Math.random() * 0.08;

      // Temperature is the inverse of coherence
      const calculatedTemp = Math.max(0, 1 - coherence);

      setHistory((prev) => {
        const newPulse = [...prev.pulse.slice(1), Math.min(60, fps)];
        const newPressure = [...prev.pressure.slice(1), simulatedPressure];
        const newTemp = [...prev.temp.slice(1), calculatedTemp];
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
