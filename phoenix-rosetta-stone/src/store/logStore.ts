
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { ExperienceLog } from '@essence/types';

interface LogState {
  isGenerating: boolean;
  lastLog: ExperienceLog | null;
  logs: ExperienceLog[];
  setGenerating: (isGenerating: boolean) => void;
  addLog: (log: ExperienceLog) => void;
}

export const useLogStore = create<LogState>()(
  persist(
    (set) => ({
      isGenerating: false,
      lastLog: null,
      logs: [],
      setGenerating: (isGenerating) => set({ isGenerating }),
      addLog: (log) => set((state) => ({ 
        lastLog: log, 
        logs: [log, ...state.logs].slice(0, 100) // Anchor up to 100 interaction units
      })),
    }),
    {
      name: 'phoenix-omni-log-anchor',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ 
        logs: state.logs,
        lastLog: state.lastLog 
      }),
    }
  )
);
