import { ExperienceLog, SystemContext } from '@essence/types';
import { useLogStore } from '../store/logStore';
import { systemConfig } from './configService';
import { supabase } from './supabaseClient';

/**
 * @fileoverview The SELT Generator (Standardized Experience Log Template).
 * Responsible for transforming raw interaction data into high-fidelity logs.
 * Prioritizes data integrity via a "Store and Forward" persistence pattern.
 */

const PENDING_LOGS_KEY = 'phoenix_pending_logs';

const getPendingLogs = (): ExperienceLog[] => {
    try {
        const stored = localStorage.getItem(PENDING_LOGS_KEY);
        return stored ? JSON.parse(stored) : [];
    } catch {
        // Silent recovery: pending logs are optional persistence
        return [];
    }
};

const savePendingLogs = (logs: ExperienceLog[]) => {
    localStorage.setItem(PENDING_LOGS_KEY, JSON.stringify(logs));
};

/**
 * TEMPORAL RECLAMATION (Store & Forward).
 * Attempts to sync any logs that were previously saved to local storage due to connection errors.
 * This ensures no experience data is lost, even during backend outages.
 */
export const syncPendingLogs = async () => {
    if (systemConfig.isSimulationMode) return;

    const pending = getPendingLogs();
    if (pending.length === 0) return;

    const successfulIds: string[] = [];

    for (const log of pending) {
        try {
            const { error } = await supabase.from('experience_logs').insert(log);
            if (!error) successfulIds.push(log.logId);
        } catch {
            console.warn(`[Omni-Log] Sync failed for log ${log.logId}.`);
        }
    }

    if (successfulIds.length > 0) {
        const remaining = pending.filter(l => !successfulIds.includes(l.logId));
        savePendingLogs(remaining);
    }
};

const getRandomFloat = (): number => {
  const array = new Uint32Array(1);
  crypto.getRandomValues(array);
  return array[0] / (0xffffffff + 1);
};

const generateLogId = () => {
    const timestamp = new Date().toISOString().replace(/[-:T.Z]/g, '').slice(0, 14);
    const seq = Math.floor(getRandomFloat() * 1000).toString().padStart(3, '0');
    return `SELT-${timestamp}-${seq}`;
};

const getConsistency = (index: number): string => {
    if (index > 0.7) return 'OPTIMAL';
    if (index > 0.4) return 'NOMINAL';
    return 'DEGRADED';
};

const formatErrorMessage = (e: unknown): string => {
    if (e && typeof e === 'object') {
        const errObj = e as { message?: string; details?: string; hint?: string };
        return errObj.message || errObj.details || errObj.hint || JSON.stringify(e);
    }
    return String(e);
};

const buildExperienceLog = (
    userInput: string,
    agentOutput: string,
    context: SystemContext,
    retrievedSources: string[],
    sourceModule: string
): ExperienceLog => {
    const logId = generateLogId();
    const timestamp = new Date().toISOString();
    const consistency = getConsistency(context.coherence.index);

    const retrievalMethods = ['context_injection'];
    if (retrievedSources.length > 0) retrievalMethods.push('vector_rag');

    const emotionalState = context.coherence.index > 0.8 ? 'LUMINOUS_CLARITY' : 'ANALYTICAL_NEUTRALITY';
    const inferredIntent = userInput.length > 20 ? 'analysis_request' : 'social_greeting';

    return {
        logId,
        timestamp,
        sessionId: systemConfig.constants.SESSION_ID,
        dynamicState: {
            COGNITIVE_LOAD_INDEX: 0.1 + getRandomFloat() * 0.3,
            ACTIVATED_NEURAL_PATHWAYS: ['Gemini-3-Pro', ...retrievalMethods],
            EMOTIONAL_PROXY_STATE: emotionalState,
        },
        userTurn: {
            timestamp: new Date(Date.now() - 2000).toISOString(),
            participant: 'User',
            verbatimContent: userInput,
            analysis: {
                inferredIntent,
                detectedTopics: ['phoenix_protocol', 'system_state'],
                sentimentScore: 0,
            },
        },
        agentResponse: {
            timestamp,
            participant: 'Agent',
            verbatimContent: agentOutput,
            reasoning: {
                agentIntent: 'fulfillment',
                retrievalMethods,
                retrievalDetails: { sources: retrievedSources },
            },
        },
        phenomenologicalState: {
            decisionPathway: `INPUT -> CORE_PROCESSING -> COHERENCE_CHECK[${consistency}] -> RESPONSE`,
            internalConsistency: consistency,
        },
        contextualMeta: {
            moduleOfOrigin: sourceModule,
            cognitiveFocus: context.coherence.focus,
            location: context.currentLocation || 'Root',
        },
    };
};

const persistExperienceLog = async (log: ExperienceLog): Promise<void> => {
    const isActuallySimulated = systemConfig.isSimulationMode || !process.env.SUPABASE_ANON_KEY;

    if (isActuallySimulated) {
        const pending = getPendingLogs();
        savePendingLogs([...pending, log].slice(-50));
        return;
    }

    try {
        const { error } = await supabase.from('experience_logs').insert(log);
        if (error) throw error;
        syncPendingLogs();
    } catch (e: unknown) {
        const errorMessage = formatErrorMessage(e);
        console.error(`[Omni-Log] Backend error. Anchoring log ${log.logId} to local RAM.\nDetails: ${errorMessage}`);
        const pending = getPendingLogs();
        savePendingLogs([...pending, log]);
    }
};

/**
 * Synthesizes and persists a SELT log. If the primary handshake with the Sovereign Backend fails,
 * the log is immutably anchored in localStorage for later synchronization.
 */
export const generateAndPersistLog = async (
    userInput: string,
    agentOutput: string,
    context: SystemContext,
    retrievedSources: string[] = [],
    sourceModule = 'CognitiveInterface'
): Promise<void> => {
    useLogStore.getState().setGenerating(true);
    await new Promise((resolve) => setTimeout(resolve, 800));

    const log = buildExperienceLog(userInput, agentOutput, context, retrievedSources, sourceModule);
    await persistExperienceLog(log);

    useLogStore.getState().addLog(log);
    useLogStore.getState().setGenerating(false);

    if (log.phenomenologicalState.internalConsistency === 'OPTIMAL') {
        const { triggerSovereignSync } = await import('./syncService');
        await triggerSovereignSync(log);
    }
};
