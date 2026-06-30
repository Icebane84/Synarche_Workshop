import { WeaverValue } from '@essence/types';

export enum SignalType {
    // Core System Signals
    CORE_AWAKEN = 'CORE_AWAKEN',
    CORE_STABILIZED = 'CORE_STABILIZED',
    
    // Command & Intent Signals
    SYNERGY_FIRE = 'SYNERGY_FIRE',
    SYNERGY_RESULT = 'SYNERGY_RESULT',
    
    // Aesthetic & Resonance Signals
    COHERENCE_RIPPLE = 'COHERENCE_RIPPLE',
    AURAL_ECHO = 'AURAL_ECHO',
    NOVA_SPARK_EMITTED = 'NOVA_SPARK_EMITTED',
    VAULT_CONTEXT_READY = 'VAULT_CONTEXT_READY'
}

/**
 * Maps each SignalType to its required payload structure.
 */
export interface SignalPayloads {
    [SignalType.CORE_AWAKEN]: undefined;
    [SignalType.CORE_STABILIZED]: undefined;
    [SignalType.SYNERGY_FIRE]: { commandId?: string; params?: Record<string, WeaverValue>; chain?: string[] };
    [SignalType.SYNERGY_RESULT]: { success: boolean; message?: string; chain?: boolean };
    [SignalType.COHERENCE_RIPPLE]: { intensity: number };
    [SignalType.AURAL_ECHO]: { type: string };
    [SignalType.NOVA_SPARK_EMITTED]: { x: number; y: number; color?: string };
    [SignalType.VAULT_CONTEXT_READY]: { query: string; resultsCount: number; data?: unknown };
}

export interface SignalData<T extends SignalType = SignalType> {
    type: T;
    payload?: SignalPayloads[T];
    meta?: {
        isGlobal?: boolean;
        origin?: string;
        timestamp?: number;
    };
}

class SovereignSignalBus extends EventTarget {
    private static instance: SovereignSignalBus;

    private constructor() {
        super();
    }

    public static getInstance(): SovereignSignalBus {
        if (!SovereignSignalBus.instance) {
            SovereignSignalBus.instance = new SovereignSignalBus();
        }
        return SovereignSignalBus.instance;
    }

    /**
     * Broadcast a signal onto the bus.
     */
    public emit<T extends SignalType>(
        type: T, 
        payload?: SignalPayloads[T], 
        meta?: SignalData<T>['meta']
    ): void {
        const event = new CustomEvent(type, {
            detail: {
                type,
                payload,
                meta: {
                    isGlobal: true,
                    origin: 'Nexus',
                    timestamp: Date.now(),
                    ...meta
                }
            }
        });
        this.dispatchEvent(event);
    }

    /**
     * Listen for a specific signal.
     */
    public on<T extends SignalType>(
        type: T, 
        callback: (data: SignalData<T>) => void
    ): () => void {
        const wrapper = (event: Event) => {
            const customEvent = event as CustomEvent<SignalData<T>>;
            callback(customEvent.detail);
        };

        this.addEventListener(type, wrapper);
        
        // Return unsubscribe function
        return () => {
            this.removeEventListener(type, wrapper);
        };
    }
}

// Export singleton instance
export const signalBus = SovereignSignalBus.getInstance();
