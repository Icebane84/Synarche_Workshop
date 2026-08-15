import { RealtimeChannel } from '@supabase/supabase-js';
import { create } from 'zustand';
import { supabase } from '../services/supabaseClient';
import { Task, TaskPriority, TaskSource, TaskStatus } from '@essence/types';
import { useCoherenceStore } from './coherenceStore';

interface TaskState {
    /** The primary array of tasks, sorted by timestamp (newest first). */
    tasks: Task[];
    /** Indicates if the system is currently handshaking with Supabase. */
    isLoading: boolean;
    /**
     * simulationMode: When true, the system operates on local RAM only (Mock Data).
     * Activated automatically on connection failure.
     */
    isSimulationMode: boolean;
    /** Diagnostic message for the last known error (e.g., "Schema Dissonance"). */
    error: string | null;
    /** The active Supabase Realtime subscription channel. */
    realtimeChannel: RealtimeChannel | null;
    /** Current state of the backend connection. */
    connectionStatus: 'disconnected' | 'connecting' | 'connected' | 'degraded';

    /**
     * ESTABLISH HANDSHAKE:
     * Connects to the Sovereign Backend (Supabase).
     * If the connection fails or the table is missing, it gracefully degrades to Simulation Mode.
     */
    initialize: () => Promise<void>;

    /**
     * Adds a new task to The Loom.
     * Uses "Optimistic UI" updates for instant feedback, then syncs with backend.
     */
    addTask: (taskData: {
        title: string;
        notes: string;
        source: TaskSource;
        priority?: TaskPriority;
    }) => Promise<Task | null>;

    updateTaskStatus: (taskId: string, status: TaskStatus) => Promise<void>;
    updateTaskNotes: (taskId: string, notes: string) => Promise<void>;
    updateTask: (taskId: string, updates: Partial<Task>) => Promise<void>;

    deleteTask: (taskId: string) => Promise<void>;
    addTaskLog: (
        taskId: string,
        entry: { action: 'Fixed Error' | 'Caused Error' | 'Comment'; details: string },
    ) => Promise<void>;

    /** Activates the real-time neural link for live updates from other clients. */
    subscribe: () => void;
    unsubscribe: () => void;

    /** Explicit action to force the system into Simulation Mode (Sandbox). */
    enableSimulationMode: () => void;

    /** Triggers the autonomous repair service for a specific task. */
    resolveDissonance: (taskId: string) => Promise<{ success: boolean; message: string }>;

    /** Batch status updates across multiple tasks. */
    batchUpdateStatus: (taskIds: string[], status: TaskStatus) => Promise<void>;
    /** Batch delete across multiple tasks. */
    batchDeleteTasks: (taskIds: string[]) => Promise<void>;
    /** Purges mock and simulation tasks. */
    purgeSimulationTasks: () => Promise<void>;
    /** Automatically resolves all high-priority dissonance scanner tasks. */
    autoRepairAllHigh: () => Promise<{ resolved: number; failed: number }>;
}

const MOCK_TASKS: Task[] = [
    {
        id: 'TASK-SIM-001',
        title: 'Calibrate Coherence Matrix',
        notes: 'Initial system calibration to ensure baseline cognitive harmony in simulation mode.',
        status: 'Completed',
        source: 'Manual',
        priority: 'High',
        timestamp: Date.now() - 3600000,
    },
    {
        id: 'TASK-SIM-002',
        title: 'Analyze Neural Link Latency',
        notes: 'Detecting minor delays in synaptic transmission. Backend unreachable, running in local RAM.',
        status: 'In Progress',
        source: 'Dissonance Scanner',
        priority: 'Medium',
        timestamp: Date.now() - 1800000,
    },
];

export const useTaskStore = create<TaskState>((set, get) => {
    // Hoisted helper functions to avoid nesting depth issues (S2004)
    const handleInsert = (payload: { new: Record<string, unknown> }) => {
        const payloadTask = payload.new as unknown as Task & { timestamp: string | number };
        const rawId = payloadTask.id ? String(payloadTask.id).trim() : '';
        const id = rawId !== '' ? rawId : `TASK-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
        const newTask = {
            ...payloadTask,
            id,
            timestamp: new Date(payloadTask.timestamp).getTime(),
        } as Task;

        set((state) => {
            if (state.tasks.some((t) => t.id === newTask.id)) return state;
            return { tasks: [newTask, ...state.tasks] };
        });
        useCoherenceStore.getState().addNovaSpark(`Neural Sync: New task woven into The Loom.`);
    };

    const handleUpdate = (payload: { new: Record<string, unknown> }) => {
        const payloadTask = payload.new as unknown as Task & { timestamp: string | number };
        const rawId = payloadTask.id ? String(payloadTask.id).trim() : '';
        const id = rawId !== '' ? rawId : `TASK-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
        const updatedTask = {
            ...payloadTask,
            id,
            timestamp: new Date(payloadTask.timestamp).getTime(),
        } as Task;

        set((state) => ({
            tasks: state.tasks.map((t) => (t.id === updatedTask.id ? updatedTask : t)),
        }));
    };

    const handleDelete = (payload: { old: Record<string, unknown> }) => {
        const deletedId = payload.old.id as string;
        set((state) => ({
            tasks: state.tasks.filter((t) => t.id !== deletedId),
        }));
        useCoherenceStore.getState().addNovaSpark(`Neural Sync: Task purged from The Loom.`);
    };

    return {
        tasks: [],
        isLoading: true,
        isSimulationMode: true,
        error: null,
        realtimeChannel: null,
        connectionStatus: 'disconnected',

        initialize: async () => {
            try {
                set({ isLoading: true, error: null, connectionStatus: 'connecting' });

                const { data, error: fetchError } = await supabase
                    .from('tasks')
                    .select('*')
                    .order('timestamp', { ascending: false });

                if (fetchError) throw fetchError;

                const seenIds = new Set<string>();
                const fetchedTasks: Task[] = [];

                for (const item of (data ?? [])) {
                    const rawId = item.id ? String(item.id).trim() : '';
                    let id = rawId !== '' ? rawId : `TASK-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
                    if (seenIds.has(id)) {
                        id = `${id}-${Math.random().toString(36).slice(2, 6)}`;
                    }
                    seenIds.add(id);
                    fetchedTasks.push({
                        ...item,
                        id,
                        timestamp: new Date(item.timestamp as string | number).getTime(),
                    } as Task);
                }

                set({ 
                    tasks: fetchedTasks, 
                    isLoading: false, 
                    isSimulationMode: false,
                    connectionStatus: 'connected'
                });
                
                useCoherenceStore
                    .getState()
                    .addNovaSpark('Sovereign Backend: Handshake Successful. Connection Stabilized.');

                // Ensure we are subscribed to realtime updates
                get().subscribe();
            } catch (err: unknown) {
                // Robust error extraction for Nova Sparks
                let errorMessage = 'Unknown Error';
                if (err instanceof Error) {
                    errorMessage = err.message;
                } else if (err && typeof err === 'object' && 'message' in err) {
                    errorMessage = String((err as any).message);
                } else {
                    errorMessage = String(err);
                }

                console.warn(`[Sovereign Backend] Handshake Failed: ${errorMessage}`);

                let diagnostic = errorMessage;
                if (errorMessage.includes('relation "tasks" does not exist')) {
                    diagnostic = "Schema Dissonance: Table 'tasks' missing in Supabase.";
                } else if (errorMessage.includes('fetch')) {
                    diagnostic = "Connectivity Error: Failed to reach the Sovereign Backend.";
                }

                set({
                    isLoading: false,
                    error: diagnostic,
                    isSimulationMode: true,
                    tasks: MOCK_TASKS,
                    connectionStatus: 'degraded'
                });

                useCoherenceStore
                    .getState()
                    .addNovaSpark(`⚠️ BACKEND ALERT: ${String(diagnostic)} Running in Local Emulation.`);
            }
        },

        addTask: async (taskData) => {
            const uniqueSuffix = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
            const newTask: Task = {
                id: `TASK-${uniqueSuffix}`,
                timestamp: Date.now(),
                status: 'To Do',
                title: taskData.title,
                notes: taskData.notes,
                source: taskData.source,
                priority: taskData.priority ?? 'Medium',
            };

            // Optimistic Update: Always update local state immediately
            set((state) => {
                const filtered = state.tasks.filter((t) => t.id !== newTask.id);
                return { tasks: [newTask, ...filtered] };
            });

            if (get().isSimulationMode) {
                return newTask;
            }

            // 2. PERSISTENCE LAYER SYNC
            try {
                const { error } = await supabase.from('tasks').insert({
                    ...newTask,
                    timestamp: new Date(newTask.timestamp).toISOString(),
                });

                if (error) throw error;

                // Success: The Realtime subscription will fire 'handleInsert',
                // but our duplicate check (state.tasks.some) leads to a graceful no-op.
                return newTask;
            } catch (error: unknown) {
                console.error('[The Loom] Write Error:', error instanceof Error ? error.message : String(error));

                // Revert Optimistic Update on Failure
                set((state) => ({
                    tasks: state.tasks.filter((t) => t.id !== newTask.id),
                }));

                return null;
            }
        },

        updateTaskStatus: async (taskId, status) => {
            set((state) => ({
                tasks: state.tasks.map((task) => {
                    if (task.id === taskId) {
                        const logEntry = {
                            timestamp: Date.now(),
                            action: 'Status Change',
                            details: `Status transitioned to ${String(status)}`,
                        } as const;
                        return {
                            ...task,
                            status,
                            auditLog: task.auditLog ? [logEntry, ...task.auditLog] : [logEntry],
                        };
                    }
                    return task;
                }),
            }));

            if (!get().isSimulationMode) {
                await supabase.from('tasks').update({ status }).eq('id', taskId);
            }
        },

        updateTaskNotes: async (taskId, notes) => {
            set((state) => ({
                tasks: state.tasks.map((task) => (task.id === taskId ? { ...task, notes } : task)),
            }));

            if (!get().isSimulationMode) {
                await supabase.from('tasks').update({ notes }).eq('id', taskId);
            }
        },

        updateTask: async (taskId, updates) => {
            set((state) => ({
                tasks: state.tasks.map((task) => (task.id === taskId ? { ...task, ...updates } : task)),
            }));

            if (!get().isSimulationMode) {
                await supabase.from('tasks').update(updates).eq('id', taskId);
            }
        },

        deleteTask: async (taskId: string) => {
            set((state) => ({
                tasks: state.tasks.filter((t) => t.id !== taskId),
            }));

            if (!get().isSimulationMode) {
                await supabase.from('tasks').delete().eq('id', taskId);
            }
        },

        addTaskLog: async (
            taskId: string,
            entry: { action: 'Fixed Error' | 'Caused Error' | 'Comment'; details: string },
        ) => {
            const timestamp = Date.now();
            const fullEntry = { ...entry, timestamp, action: entry.action };

            set((state) => ({
                tasks: state.tasks.map((task) => {
                    if (task.id === taskId) {
                        return {
                            ...task,
                            auditLog: task.auditLog ? [fullEntry, ...task.auditLog] : [fullEntry],
                        };
                    }
                    return task;
                }),
            }));

            // Persist log if not in simulation mode (Requires 'audit_log' column or JSONB update)
            // For now, we assume 'auditLog' is part of the task JSON or separate table.
            // If 'auditLog' is a JSONB column in Supabase 'tasks' table, we can update it.
            // Checking schema assumption: 'tasks' table likely needs a JSONB column 'audit_log' or similar.
            // If it doesn't exist, this might fail or be silent.
            // We'll attempt a JSONB update on the record.
            if (!get().isSimulationMode) {
                // Fetch current to append? Or Supabase has append?
                // JSONB append is tricky without RPC.
                // Simplified: We accept that we overwrite the array with the new local state.
                const task = get().tasks.find((t) => t.id === taskId);
                if (task) {
                    await supabase.from('tasks').update({ audit_log: task.auditLog }).eq('id', taskId);
                }
            }
        },

        subscribe: () => {
            const { isSimulationMode, realtimeChannel } = get();
            if (isSimulationMode || realtimeChannel) return;

            const channel = supabase
                .channel('tasks-granular')
                .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'tasks' }, handleInsert)
                .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'tasks' }, handleUpdate)
                .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'tasks' }, handleDelete)
                .subscribe();

            set({ realtimeChannel: channel });
        },

        unsubscribe: () => {
            const { realtimeChannel } = get();
            if (realtimeChannel) {
                void supabase.removeChannel(realtimeChannel);
                set({ realtimeChannel: null });
            }
        },

        enableSimulationMode: () => {
            set({
                isSimulationMode: true,
                isLoading: false,
                error: 'Simulation Mode Activated by User Override.',
                tasks: MOCK_TASKS,
            });
            useCoherenceStore.getState().addNovaSpark('Simulation Mode: Synthetic Data Stream Active.');
        },

        resolveDissonance: async (taskId) => {
            const { resolveDissonance: serviceResolve } = await import('../services/repairService');
            return serviceResolve(taskId);
        },

        batchUpdateStatus: async (taskIds, status) => {
            const idSet = new Set(taskIds);
            set((state) => ({
                tasks: state.tasks.map((t) => (idSet.has(t.id) ? { ...t, status } : t)),
            }));
            if (!get().isSimulationMode) {
                try {
                    await supabase.from('tasks').update({ status }).in('id', taskIds);
                } catch (e) {
                    console.error('[The Loom] Batch status update failed:', e);
                }
            }
            useCoherenceStore.getState().addNovaSpark(`Batch Update: ${taskIds.length} tasks transitioned to ${status}.`);
        },

        batchDeleteTasks: async (taskIds) => {
            const idSet = new Set(taskIds);
            set((state) => ({
                tasks: state.tasks.filter((t) => !idSet.has(t.id)),
            }));
            if (!get().isSimulationMode) {
                try {
                    await supabase.from('tasks').delete().in('id', taskIds);
                } catch (e) {
                    console.error('[The Loom] Batch delete failed:', e);
                }
            }
            useCoherenceStore.getState().addNovaSpark(`Batch Purge: ${taskIds.length} tasks removed from the weave.`);
        },

        purgeSimulationTasks: async () => {
            set((state) => ({
                tasks: state.tasks.filter((t) => !t.id.startsWith('TASK-SIM-')),
            }));
            useCoherenceStore.getState().addNovaSpark('Loom Purge: Simulation artifacts cleared.');
        },

        autoRepairAllHigh: async () => {
            const highTasks = get().tasks.filter(
                (t) => t.priority === 'High' && t.status !== 'Completed' && t.source === 'Dissonance Scanner'
            );
            let resolved = 0;
            let failed = 0;
            const { resolveDissonance: serviceResolve } = await import('../services/repairService');

            for (const t of highTasks) {
                try {
                    const result = await serviceResolve(t.id);
                    if (result.success) {
                        resolved++;
                    } else {
                        failed++;
                    }
                } catch {
                    failed++;
                }
            }
            useCoherenceStore.getState().addNovaSpark(`Auto-Repair Complete: ${resolved} resolved, ${failed} unresolvable.`);
            return { resolved, failed };
        },
    };
});
