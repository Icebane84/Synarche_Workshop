// [OMEGA AST Cleaned]: Tokenized design standards applied.
import React, { useEffect } from 'react';
import { useTaskStore } from '../store/taskStore';
import { useSensoryStore } from '../store/sensoryStore';
import { useCoherenceStore } from '../store/coherenceStore';
import { useMemoryStore } from '../store/memoryStore';
import { useFileSystemStore } from '../store/fileSystemStore';
import { CSEBridgeService } from '../services/cseBridgeService';

/**
 * SystemManager [OMEGA v15.5]
 * Centralized orchestrator for global system initialization, 
 * heartbeat monitoring, and sovereign backend synchronization.
 */
export const SystemManager: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const initializeTasks = useTaskStore((state) => state.initialize);
    const subscribeTasks = useTaskStore((state) => state.subscribe);
    const unsubscribeTasks = useTaskStore((state) => state.unsubscribe);
    
    const initializeSensors = useSensoryStore((state) => state.initializeSensors);
    const initializeMemory = useMemoryStore((state) => state.fetchMemories);
    
    const { 
        maintenanceMode, 
        isRepairing, 
        setRepairing,
        addNovaSpark,
        updateFromTelemetry,
        setConnectionState
    } = useCoherenceStore();

    // --- LIVE TELEMETRY BRIDGE (CSE SERVER) ---
    useEffect(() => {
        const stopStream = CSEBridgeService.startTelemetryStream(
            (data) => {
                updateFromTelemetry(data);
                useFileSystemStore.getState().connectPolyglotBridge();
            },
            () => {
                setConnectionState('RECONNECTING');
            },
            2500
        );

        return () => {
            stopStream();
        };
    }, [updateFromTelemetry, setConnectionState]);

    useEffect(() => {
        let isMounted = true;

        const bootSequence = async () => {
            if (!isMounted) return;
            
            addNovaSpark('Initializing Phoenix Protocol Substrates...');

            // 1. Initialize Memory Palace (Historical Context)
            try {
                await initializeMemory();
            } catch (e) {
                console.warn('[SystemManager] Memory Palace Initialization Degraded:', e);
            }

            // 2. Initialize The Loom (Task Persistence)
            try {
                await initializeTasks();
                subscribeTasks();
            } catch (e) {
                console.error('[SystemManager] The Loom Handshake Failed:', e);
            }

            // 3. Initialize Sensory Array (VFX/SFX Resonance)
            const cleanupSensors = initializeSensors();

            addNovaSpark('System Coherence Established. All layers synchronized.');

            return cleanupSensors;
        };

        const cleanupPromise = bootSequence();

        return () => {
            isMounted = false;
            unsubscribeTasks();
            cleanupPromise.then(cleanup => cleanup && cleanup());
        };
    }, [initializeTasks, subscribeTasks, unsubscribeTasks, initializeSensors, initializeMemory, addNovaSpark]);

    // --- SYSTEM PULSE: AUTONOMOUS MAINTENANCE ---
    useEffect(() => {
        const pulseInterval = setInterval(async () => {
            if (maintenanceMode === 'Sovereign' && !isRepairing) {
                setRepairing(true);
                try {
                    const { autoRepairApprovedTasks } = await import('../services/repairService');
                    const result = await autoRepairApprovedTasks(true);
                    if (result.count > 0) {
                        addNovaSpark(`Autonomous Repair cycle complete. Resolved ${result.count} dissonances.`);
                    }
                } catch (e) {
                    console.error('[SystemManager] Autonomous Repair Fault:', e);
                } finally {
                    setRepairing(false);
                }
            }
        }, 30000); // 30-second pulse

        return () => { clearInterval(pulseInterval); };
    }, [maintenanceMode, isRepairing, setRepairing, addNovaSpark]);

    return <>{children}</>;
};


export default SystemManager;
