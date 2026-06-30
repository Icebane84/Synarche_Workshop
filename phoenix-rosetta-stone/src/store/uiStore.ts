import { create } from 'zustand';

interface UIState {
  isSynapseOpen: boolean;
  stylePatches: Record<string, string>;
  toggleSynapse: () => void;
  openSynapse: () => void;
  closeSynapse: () => void;
  applyPatch: (key: string, value: string) => void;
}

export const useUIStore = create<UIState>((set) => ({
  isSynapseOpen: false,
  stylePatches: {},
  toggleSynapse: () => { set((state) => ({ isSynapseOpen: !state.isSynapseOpen })); },
  openSynapse: () => { set({ isSynapseOpen: true }); },
  closeSynapse: () => { set({ isSynapseOpen: false }); },
  applyPatch: (key, value) => { set((state) => ({
    stylePatches: { ...state.stylePatches, [key]: value }
  })); },
}));