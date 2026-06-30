/**
 * @fileoverview useSignal Hook [PRS-002]
 * Provides a React-friendly interface for the Sovereign SignalBus.
 */

import { useEffect, useCallback } from 'react';
import { signalBus, SignalType, SignalData, SignalPayloads } from '@system/signalBus';

/**
 * Hook to subscribe to a specific SignalBus event.
 * @param type The type of signal to listen for.
 * @param callback Function to execute when the signal is detected.
 * @param deps Dependency array for the callback.
 */
export function useSignal<T extends SignalType>(
    type: T, 
    callback: (data: SignalData<T>) => void,
    deps: any[] = []
): void {
    const memoizedCallback = useCallback(callback, deps);

    useEffect(() => {
        // Subscribe to the signal bus
        const unsubscribe = signalBus.on(type, (data) => {
            memoizedCallback(data);
        });

        // Cleanup on unmount
        return () => {
            unsubscribe();
        };
    }, [type, memoizedCallback]);
}

/**
 * Hook to emit signals from a component.
 */
export function useEmitSignal() {
    return useCallback(<T extends SignalType>(
        type: T, 
        payload?: SignalPayloads[T], 
        meta?: SignalData<T>['meta']
    ) => {
        signalBus.emit(type, payload, meta);
    }, []);
}
