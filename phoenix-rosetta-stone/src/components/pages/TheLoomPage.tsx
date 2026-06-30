import { AlertTriangle, Clock, Kanban, Loader, RefreshCw, Search, Shield, ShieldAlert, ShieldCheck } from 'lucide-react';
import React, { useEffect, useMemo, useState } from 'react';
import { useSensoryResonance } from '../../hooks/useSensoryResonance';
import { useSensoryStore } from '../../store/sensoryStore';
import { useTaskStore } from '../../store/taskStore';
import { TaskSource, TaskStatus } from '@essence/types';
import { useCoherenceStore, MaintenanceMode } from '../../store/coherenceStore';

// Modular Components
import { AnimatePresence, motion } from 'framer-motion';
import ChronosTimeline from '../ChronosTimeline';
import Tooltip from '../common/Tooltip';
import { KanbanColumn } from '../loom/KanbanColumn';
import { TaskDetailsModal } from '../loom/TaskDetailsModal';

/**
 * The Loom Page [OMEGA v15.0]
 * Orchestrates the "Thought Wefts" through Logic (Kanban) and Time (Chronos).
 * Integrated with Sensory Resonance.
 */

const COLUMNS: TaskStatus[] = ['To Do', 'In Progress', 'Completed'];

const TheLoomPage: React.FC = () => {
    // Stores
    const updateTaskStatus = useTaskStore((state) => state.updateTaskStatus);
    const updateTaskNotes = useTaskStore((state) => state.updateTaskNotes);
    const tasks = useTaskStore((state) => state.tasks);
    const isLoading = useTaskStore((state) => state.isLoading);
    const isSimulationMode = useTaskStore((state) => state.isSimulationMode);
    const connectionStatus = useTaskStore((state) => state.connectionStatus);
    const error = useTaskStore((state) => state.error);
    const initialize = useTaskStore((state) => state.initialize);
    const subscribe = useTaskStore((state) => state.subscribe);
    const unsubscribe = useTaskStore((state) => state.unsubscribe);
    const deleteTask = useTaskStore((state) => state.deleteTask);

    // Coherence Store (Autonomy)
    const maintenanceMode = useCoherenceStore((state) => state.maintenanceMode);
    const setMaintenanceMode = useCoherenceStore((state) => state.setMaintenanceMode);

    // Sensory Extension
    const initializeSensors = useSensoryStore((state) => state.initializeSensors);
    const resonance = useSensoryResonance();

    // Local State
    const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
    const [viewMode, setViewMode] = useState<'kanban' | 'chronos'>('kanban');
    const [searchQuery, setSearchQuery] = useState('');
    const [sourceFilter] = useState<TaskSource | 'All'>('All');
    const [visibleCounts, setVisibleCounts] = useState<Record<TaskStatus, number>>({
        'To Do': 50,
        'In Progress': 50,
        Completed: 50,
    });

    // Lifecycle
    useEffect(() => {
        // No-op: SystemManager handles global initialization.
        // We just keep the hook reference for future local-only triggers if needed.
    }, []);

    // Derived Logic
    const selectedTask = useMemo(() => tasks.find((t) => t.id === selectedTaskId) ?? null, [tasks, selectedTaskId]);

    const tasksByStatus = useMemo(() => {
        const lowerQuery = searchQuery.toLowerCase();
        const grouped = { 
            'To Do': [] as typeof tasks, 
            'In Progress': [] as typeof tasks, 
            'Completed': [] as typeof tasks 
        };

        tasks.forEach((task) => {
            if (
                searchQuery &&
                !task.title.toLowerCase().includes(lowerQuery) &&
                !task.notes.toLowerCase().includes(lowerQuery)
            )
                return;
            if (sourceFilter !== 'All' && task.source !== sourceFilter) return;

            grouped[task.status].push(task);
        });

        (Object.keys(grouped) as TaskStatus[]).forEach((status) => {
            grouped[status].sort((a, b) => b.timestamp - a.timestamp);
        });
        return grouped;
    }, [tasks, searchQuery, sourceFilter]);

    // Handlers
    const handleClearCompleted = async () => {
        const completed = tasks.filter((t) => t.status === 'Completed');
        if (confirm(`Eradicate ${completed.length} completed wefts from the weave?`)) {
            for (const t of completed) await deleteTask(t.id);
        }
    };

    const handleDrop = (e: React.DragEvent<HTMLDivElement>, status: TaskStatus) => {
        const taskId = e.dataTransfer.getData('taskId');
        if (taskId) void updateTaskStatus(taskId, status);
    };

    if (isLoading) return <LoadingState />;
    if (error && tasks.length === 0) return <ErrorState error={error} retry={initialize} />;

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="h-full w-full p-6 flex flex-col transition-colors duration-1000 contain-content"
            style={{
                backgroundColor: `var(--color-void)`,
                borderColor: resonance.accentColor + '22', // Subtle transparent border
            }}
        >
            {/* Header */}
            <header className="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-6">
                <div>
                    <h2
                        className="text-4xl font-thin tracking-[0.25em] text-white transition-all duration-1000"
                        style={{ textShadow: `0 0 ${resonance.blur} ${resonance.accentColor}cc` }}
                    >
                        THE LOOM
                    </h2>
                    <div className="flex items-center gap-4 mt-3">
                        <p className="text-weft-muted text-xs uppercase tracking-widest opacity-60">
                            Thought Weft Orchestration
                        </p>
                        <ConnectionStatus status={connectionStatus} />
                        {isSimulationMode && <SimulationBadge />}
                    </div>
                </div>

                    <div className="flex flex-wrap items-center gap-4">
                        <AutonomySelector mode={maintenanceMode} setMode={setMaintenanceMode} />
                        
                        <div className="relative glass-panel px-4 py-2 flex items-center gap-3">
                            <Search size={14} className="text-weft-muted" />
                            <input
                                type="text"
                                placeholder="TRACE WEFT..."
                                value={searchQuery}
                                onChange={(e) => {
                                    setSearchQuery(e.target.value);
                                }}
                                className="bg-transparent text-xs font-mono text-weft focus:outline-none w-40 md:w-64"
                            />
                        </div>

                        <ViewModeToggle view={viewMode} setView={setViewMode} />
                    </div>
            </header>

            {/* Content Area */}
            <main className="flex-1 overflow-hidden relative">
                <AnimatePresence mode="wait">
                    {viewMode === 'kanban' ? (
                        <motion.div
                            key="kanban"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            className="h-full grid grid-cols-1 md:grid-cols-3 gap-8"
                        >
                            {COLUMNS.map((status) => (
                                <KanbanColumn
                                    key={status}
                                    status={status}
                                    tasks={tasksByStatus[status]}
                                    visibleCount={visibleCounts[status]}
                                    onSelectTask={setSelectedTaskId}
                                    onStatusChange={updateTaskStatus}
                                    onLoadMore={() => {
                                        setVisibleCounts((v) => ({ ...v, [status]: v[status] + 50 }));
                                    }}
                                    onClearCompleted={status === 'Completed' ? handleClearCompleted : undefined}
                                    onDrop={handleDrop}
                                />
                            ))}
                        </motion.div>
                    ) : (
                        <motion.div
                            key="chronos"
                            initial={{ opacity: 0, scale: 0.98 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.98 }}
                            className="h-full"
                        >
                            <ChronosTimeline tasks={tasks} />
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>

            {/* Modal */}
            <AnimatePresence>
                {selectedTask && (
                    <TaskDetailsModal
                        task={selectedTask}
                        onUpdateNotes={updateTaskNotes}
                        onClose={() => {
                            setSelectedTaskId(null);
                        }}
                    />
                )}
            </AnimatePresence>
        </motion.div>
    );
};

// --- Sub-Components (Internal) ---

const LoadingState = () => (
    <div className="h-full w-full flex flex-col items-center justify-center text-center">
        <Loader className="w-10 h-10 animate-spin mb-4 text-cyan-400" />
        <h2 className="text-xl font-thin tracking-widest text-weft">ALIGNING WEFTS</h2>
    </div>
);

const ErrorState = ({ error, retry }: { error: string; retry: () => void }) => (
    <div className="h-full w-full flex flex-col items-center justify-center p-6 text-center">
        <AlertTriangle className="w-12 h-12 text-resonant-error mb-4" />
        <p className="text-sm font-mono text-resonant-error/60 max-w-md break-all">{error}</p>
        <button
            onClick={retry}
            className="mt-8 flex items-center gap-2 px-6 py-2 glass-panel hover:bg-white/5 transition-all text-sm uppercase tracking-widest"
        >
            <RefreshCw size={16} /> Re-Sync
        </button>
    </div>
);

const SimulationBadge = () => (
    <Tooltip label="Neural Link Offline // Running High-Fidelity Local Emulation">
        <div className="px-2 py-0.5 bg-amber-500/10 border border-amber-500/20 rounded text-[9px] font-bold text-amber-500 uppercase tracking-tighter animate-pulse">
            Simulation Active
        </div>
    </Tooltip>
);

const ConnectionStatus = ({ status }: { status: 'disconnected' | 'connecting' | 'connected' | 'degraded' }) => {
    const config = {
        disconnected: { color: 'bg-gray-500', label: 'Disconnected', pulse: false },
        connecting: { color: 'bg-amber-500', label: 'Syncing...', pulse: true },
        connected: { color: 'bg-emerald-500', label: 'Backend Linked', pulse: false },
        degraded: { color: 'bg-red-500', label: 'Link Degraded', pulse: true },
    };

    const { color, label, pulse } = config[status];

    return (
        <Tooltip label={`Connection Status: ${label}`}>
            <div className="flex items-center gap-2 px-2 py-0.5 bg-white/5 border border-white/10 rounded">
                <div className={`w-1.5 h-1.5 rounded-full ${color} ${pulse ? 'animate-pulse shadow-[0_0_8px_rgba(245,158,11,0.5)]' : ''}`} />
                <span className="text-[9px] font-mono text-weft-muted uppercase tracking-tighter">{label}</span>
            </div>
        </Tooltip>
    );
};

const ViewModeToggle = ({
    view,
    setView,
}: {
    view: 'kanban' | 'chronos';
    setView: (v: 'kanban' | 'chronos') => void;
}) => (
    <div className="glass-panel p-1 flex gap-1">
        <button
            onClick={() => {
                setView('kanban');
            }}
            className={`p-2 rounded-lg transition-all ${view === 'kanban' ? 'bg-cyan-500/10 text-cyan-400 shadow-inner' : 'text-weft-muted hover:text-weft'}`}
        >
            <Kanban size={16} />
        </button>
        <button
            onClick={() => {
                setView('chronos');
            }}
            className={`p-2 rounded-lg transition-all ${view === 'chronos' ? 'bg-cyan-500/10 text-cyan-400 shadow-inner' : 'text-weft-muted hover:text-weft'}`}
        >
            <Clock size={16} />
        </button>
    </div>
);

const AutonomySelector = ({ mode, setMode }: { mode: MaintenanceMode; setMode: (m: MaintenanceMode) => void }) => {
    const modes: { id: MaintenanceMode; icon: React.ElementType; label: string; color: string }[] = [
        { id: 'Manual', icon: Shield, label: 'Manual', color: 'text-weft-muted' },
        { id: 'Permissioned', icon: ShieldAlert, label: 'Permissioned', color: 'text-amber-400' },
        { id: 'Sovereign', icon: ShieldCheck, label: 'Sovereign', color: 'text-cyan-400' },
    ];

    return (
        <div className="glass-panel p-1 flex gap-1">
            {modes.map((m) => (
                <button
                    key={m.id}
                    onClick={() => { setMode(m.id); }}
                    className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all text-[10px] uppercase tracking-widest font-mono ${
                        mode === m.id 
                            ? 'bg-white/5 ' + m.color 
                            : 'text-weft-muted hover:text-weft hover:bg-white/5'
                    }`}
                >
                    <m.icon size={12} />
                    <span className="hidden sm:inline">{m.label}</span>
                </button>
            ))}
        </div>
    );
};

export default TheLoomPage;

