// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { CognitiveFocus, CoherenceState, NovaSpark, SensoryData } from '@essence/types';

// Extending types locally for the repair state
export type MaintenanceMode = 'Manual' | 'Permissioned' | 'Sovereign';
export type ConnectionState = 'CONNECTED' | 'RECONNECTING' | 'DEGRADED' | 'OFFLINE';

export interface EnhancedCoherenceState extends CoherenceState {
    isRepairing: boolean;
    maintenanceMode: MaintenanceMode;
    connectionState: ConnectionState;
    setRepairing: (status: boolean) => void;
    setMaintenanceMode: (mode: MaintenanceMode) => void;
    setConnectionState: (state: ConnectionState) => void;
    updateFromTelemetry: (telemetry: any) => void;
    addPrestige: (amount?: number) => void;
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
            connectionState: 'OFFLINE',
            sensoryData: defaultSensoryData,

            // Actions
            setRepairing: (status) => set({ isRepairing: status }),
            setMaintenanceMode: (mode) => set({ maintenanceMode: mode }),
            setConnectionState: (connectionState) => set({ connectionState }),
            updateFromTelemetry: (telemetry) => {
                if (!telemetry) return;
                set((state) => ({
                    connectionState: telemetry.system_status === 'DEGRADED' ? 'DEGRADED' : 'CONNECTED',
                    coherenceIndex: typeof telemetry.coherence_index === 'number' ? telemetry.coherence_index : state.coherenceIndex,
                    cognitiveLoad: typeof telemetry.cognitive_load === 'number' ? telemetry.cognitive_load / 100 : state.cognitiveLoad,
                    prestigeLevel: Math.max(1, Math.floor((telemetry.prestige_score || 1000) / 500)),
                    coreStats: {
                        coherence: { value: Math.round((telemetry.coherence_index || 0.8) * 100), max: 100 },
                        synergy: { value: Math.round((telemetry.synergy_flow_rate || 0.8) * 100), max: 100 },
                        adaptability: { value: Math.round((telemetry.hybrid_model_score || 0.85) * 100), max: 100 },
                        transparency: { value: Math.round((telemetry.contextual_integrity_score || 0.9) * 100), max: 100 },
                    },
                }));
            },
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
            addPrestige: (amount = 100) => {
                set((state) => {
                    const currentXp = state.xp?.current ?? 350;
                    const nextXp = state.xp?.nextLevel ?? 1000;
                    const newXp = currentXp + amount;
                    let newLevel = state.prestigeLevel ?? 1;
                    let targetNextXp = nextXp;
                    if (newXp >= targetNextXp) {
                        newLevel += 1;
                        targetNextXp += 500;
                    }
                    return {
                        xp: { current: newXp, nextLevel: targetNextXp },
                        prestigeLevel: newLevel,
                    };
                });
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
