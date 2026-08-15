// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { knowledgeBase } from '../../data/knowledgeBase';
import { useCoherenceStore } from '../../store/coherenceStore';
import { useTaskStore } from '../../store/taskStore';
import { DispatchResult } from '@essence/types';
import { transmitAuralResponse } from '../audioService';
import { supabase } from '../supabaseClient';
import { indexKnowledgeBase } from '../vectorStore';

export const handleCloudCommand = async (
    commandId: string,
    params: Record<string, unknown>,
): Promise<DispatchResult | null> => {
    const { addNovaSpark } = useCoherenceStore.getState();

    switch (commandId) {
        case 'CMD_SYNC_PROTOCOL_LIBRARY': {
            const { isSimulationMode } = useTaskStore.getState();
            if (isSimulationMode)
                return {
                    success: false,
                    message: 'Sync aborted: System is in Simulation Mode. Sovereign Backend connection required.',
                };

            await transmitAuralResponse('Initiating knowledge hydration sequence.');
            addNovaSpark('Cloud Relay: Hydrating Sovereign pgvector store...');

            const records = knowledgeBase.map((doc) => ({
                id: doc.id,
                title: doc.title,
                content: doc.content,
                updated_at: new Date().toISOString(),
            }));

            const { error } = await supabase.from('protocol_artifacts').upsert(records);
            if (error) throw error; // The caller catches this

            addNovaSpark('Cloud Relay: Knowledge base anchored in Sovereign Backend.');
            return {
                success: true,
                message: `Successfully synchronized ${records.length.toString()} artifacts to the Cloud Relay.`,
            };
        }

        case 'CMD_INVOKE_CLOUD_FUNCTION': {
            const fnName = params.functionName as string;
            const bodyStr = (params.body as string) || '{}';

            await transmitAuralResponse(`Relaying request to cloud processor: ${fnName}`);
            addNovaSpark(`Cloud Relay: Invoking ${fnName}...`);

            try {
                let bodyObj = {};
                try {
                    bodyObj = JSON.parse(bodyStr) as Record<string, unknown>;
                } catch {
                    bodyObj = { raw: bodyStr };
                }

                const { data, error } = await (
                    supabase.functions as unknown as {
                        invoke: (name: string, options: unknown) => Promise<{ data: unknown; error: unknown }>;
                    }
                ).invoke(fnName, {
                    body: bodyObj,
                });

                if (error) throw new Error(JSON.stringify(error));
                addNovaSpark(`Cloud Relay: ${fnName} execution confirmed.`);
                return {
                    success: true,
                    message: `Function ${fnName} returned successfully.`,
                    data: { response: data },
                };
            } catch (e: unknown) {
                const msg = e instanceof Error ? e.message : String(e);
                addNovaSpark(`Cloud Relay: ${fnName} failed - ${msg}`);
                return { success: false, message: `Cloud invocation failed: ${msg}` };
            }
        }

        case 'CMD_TEST_BACKEND_HANDSHAKE': {
            await transmitAuralResponse('Testing sovereign link persistence.');
            const { error } = await supabase.from('tasks').select('count', { count: 'exact', head: true });

            if (error) return { success: false, message: `Handshake failed: ${error.message}` };

            // Handshake succeeded: Force re-initialization of the Task Store to exit Simulation Mode
            addNovaSpark('Sovereign Link: Handshake verified. Re-synchronizing Task Store...');
            await useTaskStore.getState().initialize();

            return {
                success: true,
                message: "Backend handshake confirmed. Table 'tasks' is accessible. System re-initialized.",
            };
        }

        case 'CMD_MIGRATE_TASKS': {
            const { tasks } = useTaskStore.getState();

            if (tasks.length === 0) {
                return { success: true, message: 'No local tasks to migrate.' };
            }

            await transmitAuralResponse(
                `Initiating Golden Bridge sequence. Migrating ${tasks.length.toString()} thought wefts to the Sovereign Backend.`,
            );
            addNovaSpark(`Migration: Uploading ${tasks.length.toString()} tasks to Cloud...`);

            const payload = tasks.map((t) => ({
                id: t.id,
                title: t.title,
                notes: t.notes,
                status: t.status,
                source: t.source,
                priority: t.priority,
                timestamp: new Date(t.timestamp).toISOString(),
            }));

            const { data, error } = await supabase.from('tasks').upsert(payload, { onConflict: 'id' }).select();

            if (error) {
                console.error('[Migration] Failed:', error);
                return { success: false, message: `Migration Failed: ${error.message}` };
            }

            if (data && data.length > 0) {
                addNovaSpark(`Migration: Success. ${data.length.toString()} tasks anchored in eternity.`);
                return {
                    success: true,
                    message: `Successfully migrated ${data.length.toString()} tasks to Supabase. Persistence active.`,
                };
            }
            return { success: false, message: 'Migration completed but no data returned.' };
        }

        case 'CMD_INDEX_KNOWLEDGE': {
            await transmitAuralResponse('Initiating knowledge base hydration. Generating neural embeddings.');
            addNovaSpark('System: Generating embeddings and indexing to Supabase...');

            try {
                await indexKnowledgeBase();
                addNovaSpark('System: Knowledge base successfully indexed.');
                return {
                    success: true,
                    message: 'Knowledge base successfully synchronized with Sovereign Vector Store.',
                };
            } catch (e: unknown) {
                const msg = e instanceof Error ? e.message : String(e);
                return { success: false, message: `Indexing failed: ${msg}` };
            }
        }

        default:
            return null;
    }
};

