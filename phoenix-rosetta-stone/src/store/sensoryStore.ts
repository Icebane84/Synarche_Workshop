import { create } from 'zustand';
import { fetchEnvironmentalData, getSystemTime } from '../services/sensoryService';
import { SensoryData } from '@essence/types';

/**
 * Sensory Store [OMEGA v15.0]
 * Manages live environmental presence and UI resonance states.
 */

interface SensoryState {
    data: SensoryData;
    lastUpdated: number;
    isRefreshing: boolean;
    
    // Actions
    updateSense: () => Promise<void>;
    tickTime: () => void;
    initializeSensors: () => () => void; // Returns cleanup
}

const DEFAULT_DATA: SensoryData = {
    timestamp: Date.now(),
    timeString: '--:--:--',
    location: null,
    weather: null,
    status: 'calibrating',
};

export const useSensoryStore = create<SensoryState>((set, get) => ({
    data: DEFAULT_DATA,
    lastUpdated: 0,
    isRefreshing: false,

    updateSense: async () => {
        if (get().isRefreshing) return;
        set({ isRefreshing: true });
        
        try {
            const sense = await fetchEnvironmentalData();
            set({ 
                data: {
                    ...get().data,
                    ...sense,
                    timestamp: Date.now(),
                    timeString: getSystemTime(),
                } as SensoryData,
                lastUpdated: Date.now(),
                isRefreshing: false
            });
        } catch {
            set({ isRefreshing: false });
        }
    },

    tickTime: () => {
        set((state) => ({
            data: {
                ...state.data,
                timeString: getSystemTime(),
            }
        }));
    },

    initializeSensors: () => {
        // Initial setup
        void get().updateSense();

        // 1. Time ticking (every second)
        const timeInterval = setInterval(() => {
            get().tickTime();
        }, 1000);

        // 2. Sensory refresh (every 15 minutes)
        const senseInterval = setInterval(() => {
            void get().updateSense();
        }, 15 * 60 * 1000);

        return () => {
            clearInterval(timeInterval);
            clearInterval(senseInterval);
        };
    }
}));
