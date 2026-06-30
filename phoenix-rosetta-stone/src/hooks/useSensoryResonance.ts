import { useMemo } from 'react';
import { useSensoryStore } from '../store/sensoryStore';

/**
 * useSensoryResonance Hook [OMEGA v15.0]
 * Computes UI "Mood" and design tokens based on environmental sensing.
 */

export interface ResonanceProfile {
  theme: 'void' | 'loom' | 'storm';
  blur: string;
  glowOpacity: number;
  accentColor: string;
}

export const useSensoryResonance = (): ResonanceProfile => {
  const { data } = useSensoryStore();

  const profile = useMemo((): ResonanceProfile => {
    const hour = new Date().getHours();
    const isNight = hour >= 21 || hour < 6;
    const isStormy = data.weather 
      ? [80.81, 82, 95, 96, 99].includes(data.weather.conditionCode) 
      : false;

    // 1. Theme Selection
    if (isStormy) {
      return {
        theme: 'storm',
        blur: '16px',
        glowOpacity: 0.5,
        accentColor: '#94a3b8', // Storm Gray
      };
    }

    if (isNight) {
      return {
        theme: 'void',
        blur: '24px',
        glowOpacity: 0.2,
        accentColor: '#1e1b4b', // Deep Indigo
      };
    }

    // Default: Loom (Standard Active)
    return {
      theme: 'loom',
      blur: '12px',
      glowOpacity: 0.35,
      accentColor: '#22d3ee', // Cyan
    };
  }, [data.weather]);

  return profile;
};
