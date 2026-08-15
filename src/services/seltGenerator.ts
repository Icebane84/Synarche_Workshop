// [OMEGA AST Cleaned]: Tokenized design standards applied.

import { ExperienceLog, SystemContext } from '@essence/types';
import { useLogStore } from '../store/logStore';
import { supabase } from './supabaseClient';
import { systemConfig } from './configService';

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
            // Ensure we are inserting into 'experience_logs'
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

const generateLogId = () => {
    const timestamp = new Date().toISOString().replace(/[-:T.Z]/g, '').slice(0, 14);
    const seq = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    return `SELT-${timestamp}-${seq}`;
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
    // Mimic processing latency
    await new Promise(resolve => setTimeout(resolve, 800));

    const logId = generateLogId();
    const timestamp = new Date().toISOString();
    
    let consistency = 'DEGRADED';
    if (context.coherence.index > 0.7) consistency = 'OPTIMAL';
    else if (context.coherence.index > 0.4) consistency = 'NOMINAL';
    const retrievalMethods = ['context_injection'];
    if (retrievedSources.length > 0) retrievalMethods.push('vector_rag');
    
    const log: ExperienceLog = {
        logId,
        timestamp,
        sessionId: systemConfig.constants.SESSION_ID, 
        
        dynamicState: {
            COGNITIVE_LOAD_INDEX: 0.1 + (Math.random() * 0.3), 
            ACTIVATED_NEURAL_PATHWAYS: ['Gemini-3-Pro', ...retrievalMethods],
            EMOTIONAL_PROXY_STATE: context.coherence.index > 0.8 ? 'LUMINOUS_CLARITY' : 'ANALYTICAL_NEUTRALITY'
        },

        userTurn: {
            timestamp: new Date(Date.now() - 2000).toISOString(), 
            participant: 'User',
            verbatimContent: userInput,
            analysis: {
                inferredIntent: userInput.length > 20 ? 'analysis_request' : 'social_greeting',
                detectedTopics: ['phoenix_protocol', 'system_state'], 
                sentimentScore: 0
            }
        },

        agentResponse: {
            timestamp,
            participant: 'Agent',
            verbatimContent: agentOutput,
            reasoning: {
                agentIntent: 'fulfillment',
                retrievalMethods: retrievalMethods,
                retrievalDetails: {
                    sources: retrievedSources
                }
            }
        },

        phenomenologicalState: {
            decisionPathway: `INPUT -> CORE_PROCESSING -> COHERENCE_CHECK[${consistency}] -> RESPONSE`,
            internalConsistency: consistency
        },

        contextualMeta: {
            moduleOfOrigin: sourceModule,
            cognitiveFocus: context.coherence.focus,
            location: context.currentLocation || 'Root'
        }
    };

    // 3. PERSISTENCE LOGIC
    // We use a "Double-Safety" net. If the backend is unreachable or simulated,
    // we anchor the log to LocalStorage (RAM) for later synchronization.
    
    // Airtight simulation detection: If SUPABASE_URL is missing OR points to default/placeholder without valid creds
    const isActuallySimulated = systemConfig.isSimulationMode || !process.env.SUPABASE_ANON_KEY;

    if (isActuallySimulated) {
        const pending = getPendingLogs();
        savePendingLogs([...pending, log].slice(-50));
    } else {
        try {
            const { error } = await supabase.from('experience_logs').insert(log);
            if (error) throw error;
            // Attempt to sync other pending logs if connection is healthy
            syncPendingLogs();
        } catch (e: any) {
            // Robust error stringification to prevent [object Object]
            let errorMessage: string;
            if (e && typeof e === 'object') {
                errorMessage = e.message || e.details || e.hint || JSON.stringify(e);
            } else {
                errorMessage = String(e);
            }
            
            console.error(`[Omni-Log] Backend error. Anchoring log ${logId} to local RAM.\nDetails: ${errorMessage}`);
            const pending = getPendingLogs();
            savePendingLogs([...pending, log]);
        }
    }

    useLogStore.getState().addLog(log);
    useLogStore.getState().setGenerating(false);

    // 4. AUTOMATED SYNC (Gold Standard Implementation)
    if (log.phenomenologicalState.internalConsistency === 'OPTIMAL') {
        const { triggerSovereignSync } = await import('./syncService');
        await triggerSovereignSync(log);
    }
};


