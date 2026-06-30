import { useState } from 'react';
import {
    connectLocalFsCommand,
    dispatchCommand,
    fetchArtifactMetadataCommand,
    scanLocalProjectCommand,
} from '../services';
import { useCoherenceStore } from '../store/coherenceStore';
import { useTaskStore } from '../store/taskStore';
import { DispatchResult } from '@essence/types';

/**
 * @fileoverview Hook for managing the Phoenix Protocol Ignition sequence.
 */
export const useProtocolIgnition = () => {
    const [step, setStep] = useState(1);
    const [isProcessing, setIsProcessing] = useState(false);
    const [results, setResults] = useState<Partial<Record<number, DispatchResult>>>({});
    const [ignitionLogs, setIgnitionLogs] = useState<string[]>(['Awaiting Architect authentication...']);
    const [showFixCommand, setShowFixCommand] = useState(false);
    const addNovaSpark = useCoherenceStore((state) => state.addNovaSpark);

    const addLog = (msg: string) => {
        setIgnitionLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`].slice(-10));
    };

    const runAudit = async () => {
        setIsProcessing(true);
        addLog('Structural Eye: Initiating substrate audit...');
        addLog('DEEPER_ANALYSIS: Attempting AST verification...');

        const res = await dispatchCommand(scanLocalProjectCommand, {});
        setResults((prev) => ({ ...prev, 1: res }));
        setIsProcessing(false);

        if (res.success) {
            setStep(2);
            addLog('Success: Local substrate script execution authorized.');
            addNovaSpark('Substrate Audit: Coherence Verified.');
        } else {
            addLog('ALERT: Substrate handshake failed. Local scripts restricted.');
            setShowFixCommand(true);
            // Auto-activate simulation if handshake fails to unblock UI
            useTaskStore.getState().enableSimulationMode();
            addLog('System Bypass: Simulation Mode Activated.');
        }
    };

    const runSync = async () => {
        setIsProcessing(true);
        addLog('Neural Archive: Hydrating artifact metadata...');
        const res = await dispatchCommand(fetchArtifactMetadataCommand, { artifactId: 'doc-synergies' });
        setResults((prev) => ({ ...prev, 2: res }));
        setIsProcessing(false);
        if (res.success) {
            setStep(3);
            addLog('Hydration: Neural pathways mapped to Cloud Definitions.');
            addNovaSpark('Metadata Sync: Neural pathways hydrated.');
        }
    };

    const establishLink = async () => {
        setIsProcessing(true);
        addLog('Neural Link: Establishing Physical Bridge...');
        const res = await dispatchCommand(connectLocalFsCommand, {});
        setResults((prev) => ({ ...prev, 3: res }));
        setIsProcessing(false);
        if (res.success) {
            addLog('DEEPER_ANALYSIS: Neural Link Active. Sector indexed.');
            addLog('HANDSHAKE COMPLETE: System Operational.');
        }
    };

    const copyFixCommand = () => {
        void navigator.clipboard.writeText('Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser');
        addLog('Physical Bridge: Configuration command copied to clipboard.');
    };

    return {
        step,
        isProcessing,
        results,
        ignitionLogs,
        showFixCommand,
        runAudit,
        runSync,
        establishLink,
        copyFixCommand,
    };
};
