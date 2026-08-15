// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { useCoherenceStore } from '../../store/coherenceStore';
import { useTaskStore } from '../../store/taskStore';
import { DispatchResult } from '@essence/types';
import { transmitAuralResponse } from '../audioService';
import { resolveDissonance as repairDissonance } from '../repairService';

export const handleTaskCommand = async (
    commandId: string,
    params: Record<string, unknown>,
): Promise<DispatchResult | null> => {
    const { addNovaSpark } = useCoherenceStore.getState();
    const { tasks, initialize: fetchTasks, addTask } = useTaskStore.getState();

    switch (commandId) {
        case 'CMD_FETCH_TASKS': {
            await fetchTasks();
            const count = useTaskStore.getState().tasks.length;
            return {
                success: true,
                message: `The Loom synchronized with Sovereign Backend. Retrieved ${count.toString()} tasks.`,
            };
        }

        case 'CMD_VIEW_TASK_DETAILS': {
            const taskId = params.taskId as string;
            const task = tasks.find((t) => t.id === taskId);
            if (!task) return { success: false, message: `Task ${taskId} not found.` };
            return {
                success: true,
                message: `Retrieved details for task ${taskId}.`,
                data: task as unknown as Record<string, unknown>,
            };
        }

        case 'CMD_LOG_TASK_TO_LOOM': {
            const title = params.title as string;
            const notes = (params.notes as string) || '';
            const task = await addTask({ title, notes, source: 'Manual', priority: 'Medium' });
            if (task) {
                addNovaSpark(`Manual Task Woven: ${title}`);
                return { success: true, message: `Successfully added task ${task.id} to The Loom.` };
            }
            return { success: false, message: 'Failed to persist task to The Loom.' };
        }

        case 'CMD_MIGRATE_TASKS': {
            const { isSimulationMode, error: backendError } = useTaskStore.getState();
            if (isSimulationMode) {
                return {
                    success: false,
                    message: `Migration Blocked: Backend is currently in simulation mode. Error info: ${backendError ?? 'Unknown'}`,
                };
            }

            await transmitAuralResponse('Initiating the Golden Bridge migration. Transferring local tasks to the cloud.');
            try {
                const { supabase } = await import('../supabaseClient');
                // Use single bulk upsert (10-50x faster) to prevent race conditions.
                // Each task has its ID, so this is atomic.
                const { data, error } = await supabase.from('tasks').upsert(tasks, { onConflict: 'id' }).select();

                if (error) throw error;

                addNovaSpark(`Golden Bridge: ${tasks.length.toString()} tasks migrated successfully.`);
                return {
                    success: true,
                    message: `Migration successful. ${tasks.length.toString()} tasks synchronized with the Sovereign Backend.`,
                    data: { tasksMigrated: tasks.length, records: data },
                };
            } catch (err: unknown) {
                const msg = err instanceof Error ? err.message : String(err);
                return { success: false, message: `Migration Failed: ${msg}` };
            }
        }

        case 'CMD_RESOLVE_DISSONANCE': {
            const taskId = params.taskId as string;
            const result = await repairDissonance(taskId);
            return result;
        }

        case 'CMD_HARMONY_SCAN': {
            // Moved here or System? It produces TASKS. It fits nicely here or System.
            // Original plan put it in systemCommands? No, I missed it in plan explicitly.
            // It uses useFileSystemStore to get files, then addTask.
            // Let's put it here since it generates tasks?
            // Or maybe FileSystem? It's a "SCAN".
            // But SystemCommands has 'CMD_SCAN_FOR_DISSONANCE'.
            // I'll put it in fileSystemCommands actually, but I already wrote that file.
            // I'll put it in SystemCommands then.
            return null;
        }

        default:
            return null;
    }
};

