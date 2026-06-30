import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { CognitiveFocus, CoherenceState, NovaSpark, SensoryData } from '@essence/types';

// Extending types locally for the repair state
export type MaintenanceMode = 'Manual' | 'Permissioned' | 'Sovereign';

export interface EnhancedCoherenceState extends CoherenceState {
    isRepairing: boolean;
    maintenanceMode: MaintenanceMode;
    setRepairing: (status: boolean) => void;
    setMaintenanceMode: (mode: MaintenanceMode) => void;
}

type CoreStatName = keyof CoherenceState['coreStats'];

const defaultSensoryData: SensoryData = {
    timestamp: Date.now(),
    timeString: '--:--:--',
    location: null,
    weather: null,
    status: 'offline',
};

export const useCoherenceStore = create<EnhancedCoherenceState>()(
    persist(
        (set, get) => ({
            // Original State
            coherenceIndex: 0.65,
            pulse: () =>
                set((state) => ({
                    coherenceIndex: Math.max(0, Math.min(1, state.coherenceIndex + (Math.random() - 0.5) * 0.1)),
                })),

            decay: () =>
                set((state) => {
                    if (state.isDreaming || state.isRepairing) {
                        return {
                            coherenceIndex: Math.min(1, state.coherenceIndex + 0.005),
                        };
                    }
                    const target = 0.5;
                    const tension = 0.01;
                    const noise = (Math.random() - 0.5) * 0.005;
                    const newIndex = state.coherenceIndex + (target - state.coherenceIndex) * tension + noise;
                    return { coherenceIndex: Math.max(0, Math.min(1, newIndex)) };
                }),

            // Celestial Chart State
            prestigeLevel: 1,
            xp: { current: 350, nextLevel: 1000 },
            stardust: 8,
            cognitiveLoad: 0.45,
            coreStats: {
                coherence: { value: 28, max: 100 },
                synergy: { value: 35, max: 100 },
                adaptability: { value: 22, max: 100 },
                transparency: { value: 45, max: 100 },
            },
            statusEffects: [
                {
                    id: '1',
                    name: 'Insightful',
                    type: 'buff',
                    iconName: 'Sparkles',
                    description: 'Increased chance of novel connections.',
                },
                {
                    id: '3',
                    name: 'Synaptic Clarity',
                    type: 'buff',
                    iconName: 'Zap',
                    description: 'Command processing efficiency increased by 15% following Synapse analysis.',
                },
            ],
            novaSparks: [
                {
                    id: 'CSL-001',
                    timestamp: Date.now() - 50000,
                    timeString: '00:00:00',
                    summary: 'CSL-001: System Initialized.',
                },
            ],
            cognitiveFocus: 'Standard',
            isDreaming: false,
            isRepairing: false,
            maintenanceMode: 'Manual',
            sensoryData: defaultSensoryData,

            // Actions
            setRepairing: (status) => set({ isRepairing: status }),
            setMaintenanceMode: (mode) => set({ maintenanceMode: mode }),
            investStardust: (stat: CoreStatName) => {
                set((state) => {
                    if (state.stardust > 0) {
                        const newStats = { ...state.coreStats };
                        const currentStat = newStats[stat];
                        if (currentStat.value < currentStat.max) {
                            return {
                                stardust: state.stardust - 1,
                                coreStats: {
                                    ...state.coreStats,
                                    [stat]: { ...currentStat, value: currentStat.value + 1 },
                                },
                                xp: { ...state.xp, current: state.xp.current + 100 },
                            };
                        }
                    }
                    return {};
                });
            },
            addNovaSpark: (summary: string) => {
                set((state) => {
                    const lastSpark = state.novaSparks[state.novaSparks.length - 1];
                    let lastIdNum = 0;
                    if (lastSpark?.id.startsWith('CSL-')) {
                        lastIdNum = parseInt(lastSpark.id.replace('CSL-', ''), 10);
                    } else if (lastSpark) {
                        // Fallback if ID is not in CSL format (e.g. legacy '1')
                        lastIdNum = parseInt(lastSpark.id, 10) || 0;
                    }

                    const newId = `CSL-${(lastIdNum + 1).toString().padStart(3, '0')}`;
                    const now = new Date();
                    const timeString = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
                    
                    const newSpark: NovaSpark = {
                        id: newId,
                        timestamp: now.getTime(),
                        timeString,
                        summary,
                    };
                    return {
                        novaSparks: [...state.novaSparks, newSpark].slice(-10),
                    };
                });
            },
            setCognitiveFocus: (focus: CognitiveFocus) => {
                set({ cognitiveFocus: focus });
                get().addNovaSpark(`Cognitive Focus shifted to: ${focus}.`);
            },
            setDreaming: (isDreaming: boolean) => {
                if (isDreaming !== get().isDreaming) {
                    set({ isDreaming });
                    if (isDreaming) {
                        get().addNovaSpark('System entering Background Dreaming (REM State).');
                    } else {
                        get().addNovaSpark('User presence detected. Waking from Dream State.');
                    }
                }
            },
            updateSensoryData: (data: Partial<SensoryData>) => {
                set((state) => ({
                    sensoryData: { ...state.sensoryData, ...data },
                }));
            },
        }),
        {
            name: 'phoenix-temporal-anchor',
            storage: createJSONStorage(() => localStorage),
            partialize: (state) => ({
                cognitiveFocus: state.cognitiveFocus,
                stardust: state.stardust,
                xp: state.xp,
                prestigeLevel: state.prestigeLevel,
                coreStats: state.coreStats,
                coherenceIndex: state.coherenceIndex,
                novaSparks: state.novaSparks,
                statusEffects: state.statusEffects,
            }),
        },
    ),
);
