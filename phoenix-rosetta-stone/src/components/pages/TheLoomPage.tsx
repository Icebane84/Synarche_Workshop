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
import { ASTDependencyView } from '../loom/ASTDependencyView';

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
    const deleteTask = useTaskStore((state) => state.deleteTask);
    const batchUpdateStatus = useTaskStore((state) => state.batchUpdateStatus);
    const batchDeleteTasks = useTaskStore((state) => state.batchDeleteTasks);
    const purgeSimulationTasks = useTaskStore((state) => state.purgeSimulationTasks);
    const autoRepairAllHigh = useTaskStore((state) => state.autoRepairAllHigh);

    // Coherence Store (Autonomy)
    const maintenanceMode = useCoherenceStore((state) => state.maintenanceMode);
    const setMaintenanceMode = useCoherenceStore((state) => state.setMaintenanceMode);

    // Sensory Extension
    const resonance = useSensoryResonance();

    // Local State
    const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
    const [selectedTaskIds, setSelectedTaskIds] = useState<Set<string>>(new Set());
    const [isAutoRepairing, setIsAutoRepairing] = useState(false);
    const [viewMode, setViewMode] = useState<'kanban' | 'chronos' | 'ast'>('kanban');
    const [searchQuery, setSearchQuery] = useState('');
    const [sourceFilter, setSourceFilter] = useState<TaskSource | 'All'>('All');
    const [visibleCounts, setVisibleCounts] = useState<Record<TaskStatus, number>>({
        'To Do': 50,
        'In Progress': 50,
        Completed: 50,
    });

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

    const visibleTaskIds = useMemo(() => {
        const ids: string[] = [];
        COLUMNS.forEach((status) => {
            tasksByStatus[status].slice(0, visibleCounts[status]).forEach((t) => ids.push(t.id));
        });
        return ids;
    }, [tasksByStatus, visibleCounts]);

    // Handlers
    const toggleSelectTask = (taskId: string) => {
        setSelectedTaskIds((prev) => {
            const next = new Set(prev);
            if (next.has(taskId)) {
                next.delete(taskId);
            } else {
                next.add(taskId);
            }
            return next;
        });
    };

    const handleSelectAllVisible = () => {
        if (selectedTaskIds.size >= visibleTaskIds.length && visibleTaskIds.length > 0) {
            setSelectedTaskIds(new Set());
        } else {
            setSelectedTaskIds(new Set(visibleTaskIds));
        }
    };

    const handleBatchComplete = async () => {
        if (selectedTaskIds.size === 0) return;
        await batchUpdateStatus(Array.from(selectedTaskIds), 'Completed');
        setSelectedTaskIds(new Set());
    };

    const handleBatchDelete = async () => {
        if (selectedTaskIds.size === 0) return;
        if (confirm(`Purge ${selectedTaskIds.size} selected tasks?`)) {
            await batchDeleteTasks(Array.from(selectedTaskIds));
            setSelectedTaskIds(new Set());
        }
    };

    const handleAutoRepairHigh = async () => {
        setIsAutoRepairing(true);
        try {
            await autoRepairAllHigh();
        } finally {
            setIsAutoRepairing(false);
        }
    };

    const handlePurgeSimulation = async () => {
        if (confirm('Clear synthetic simulation tasks?')) {
            await purgeSimulationTasks();
        }
    };

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
            className="h-full w-full p-6 flex flex-col transition-colors duration-1000 contain-content overflow-y-auto"
            style={{
                backgroundColor: `var(--color-void)`,
                borderColor: resonance.accentColor + '22',
            }}
        >
            {/* Header */}
            <header className="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-6">
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

                <div className="flex flex-wrap items-center gap-3">
                    <AutonomySelector mode={maintenanceMode} setMode={setMaintenanceMode} />
                    
                    <div className="relative glass-panel px-3 py-1.5 flex items-center gap-2">
                        <Search size={14} className="text-weft-muted" />
                        <input
                            type="text"
                            placeholder="TRACE WEFT..."
                            value={searchQuery}
                            onChange={(e) => {
                                setSearchQuery(e.target.value);
                            }}
                            className="bg-transparent text-xs font-mono text-weft focus:outline-none w-36 md:w-52"
                        />
                    </div>

                    <ViewModeToggle view={viewMode} setView={setViewMode} />
                </div>
            </header>

            {/* Batch Action Bar & Domain Filters */}
            <div className="mb-6 bg-black/40 border border-cyan-900/40 rounded-xl p-3 flex flex-wrap items-center justify-between gap-3 backdrop-blur-sm">
                {/* Domain Filter Tabs */}
                <div className="flex items-center gap-1.5 flex-wrap">
                    <span className="text-[10px] uppercase font-mono text-cyan-400 mr-1 tracking-wider">Source:</span>
                    {(['All', 'Dissonance Scanner', 'Manual', 'Synergy Simulator', 'Neural Link'] as const).map((src) => (
                        <button
                            key={src}
                            onClick={() => setSourceFilter(src)}
                            className={`px-2.5 py-1 rounded text-[10px] font-mono transition-all ${
                                sourceFilter === src
                                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                            }`}
                        >
                            {src}
                        </button>
                    ))}
                </div>

                {/* Batch Action Buttons */}
                <div className="flex items-center gap-2 flex-wrap">
                    <button
                        onClick={handleAutoRepairHigh}
                        disabled={isAutoRepairing}
                        className="flex items-center gap-1.5 px-3 py-1 text-[11px] font-mono rounded bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/40 transition-all disabled:opacity-50"
                    >
                        <RefreshCw size={12} className={isAutoRepairing ? 'animate-spin' : ''} />
                        <span>{isAutoRepairing ? 'Healing...' : 'Auto-Repair High'}</span>
                    </button>

                    {selectedTaskIds.size > 0 && (
                        <>
                            <button
                                onClick={handleBatchComplete}
                                className="flex items-center gap-1 px-3 py-1 text-[11px] font-mono rounded bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 transition-all"
                            >
                                <ShieldCheck size={12} />
                                <span>Complete ({selectedTaskIds.size})</span>
                            </button>

                            <button
                                onClick={handleBatchDelete}
                                className="flex items-center gap-1 px-3 py-1 text-[11px] font-mono rounded bg-red-500/10 hover:bg-red-500/20 text-red-300 border border-red-500/40 transition-all"
                            >
                                <ShieldAlert size={12} />
                                <span>Purge ({selectedTaskIds.size})</span>
                            </button>
                        </>
                    )}

                    <button
                        onClick={handlePurgeSimulation}
                        className="px-2.5 py-1 text-[10px] font-mono rounded text-slate-400 hover:text-slate-200 hover:bg-white/5 border border-slate-800 transition-all"
                    >
                        Clean Sandbox
                    </button>

                    <button
                        onClick={handleSelectAllVisible}
                        className="px-2.5 py-1 text-[10px] font-mono rounded text-cyan-400 hover:bg-cyan-500/10 border border-cyan-500/30 transition-all"
                    >
                        {selectedTaskIds.size >= visibleTaskIds.length && visibleTaskIds.length > 0 ? 'Deselect All' : 'Select All'}
                    </button>
                </div>
            </div>

            {/* Content Area */}
            <main className="flex-1 overflow-hidden relative min-h-[500px]">
                <AnimatePresence mode="wait">
                    {viewMode === 'kanban' ? (
                        <motion.div
                            key="kanban"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            className="h-full grid grid-cols-1 md:grid-cols-3 gap-6"
                        >
                            {COLUMNS.map((status) => (
                                <KanbanColumn
                                    key={status}
                                    status={status}
                                    tasks={tasksByStatus[status]}
                                    visibleCount={visibleCounts[status]}
                                    onSelectTask={setSelectedTaskId}
                                    onStatusChange={updateTaskStatus}
                                    selectedTaskIds={selectedTaskIds}
                                    onToggleSelectTask={toggleSelectTask}
                                    onLoadMore={() => {
                                        setVisibleCounts((v) => ({ ...v, [status]: v[status] + 50 }));
                                    }}
                                    onClearCompleted={status === 'Completed' ? handleClearCompleted : undefined}
                                    onDrop={handleDrop}
                                />
                            ))}
                        </motion.div>
                    ) : viewMode === 'chronos' ? (
                        <motion.div
                            key="chronos"
                            initial={{ opacity: 0, scale: 0.98 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.98 }}
                            className="h-full overflow-y-auto"
                        >
                            <ChronosTimeline tasks={tasks} />
                        </motion.div>
                    ) : (
                        <motion.div
                            key="ast"
                            initial={{ opacity: 0, y: 15 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -15 }}
                            className="h-full overflow-y-auto"
                        >
                            <ASTDependencyView />
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

import ASTHeatmapVisualizer from '../ast/ASTHeatmapVisualizer';
import { Layers } from 'lucide-react';

const ViewModeToggle = ({
    view,
    setView,
}: {
    view: 'kanban' | 'chronos' | 'ast';
    setView: (v: 'kanban' | 'chronos' | 'ast') => void;
}) => (
    <div className="glass-panel p-1 flex gap-1">
        <Tooltip label="Logic Matrix (Kanban)">
            <button
                onClick={() => {
                    setView('kanban');
                }}
                className={`p-2 rounded-lg transition-all ${view === 'kanban' ? 'bg-cyan-500/10 text-cyan-400 shadow-inner' : 'text-weft-muted hover:text-weft'}`}
            >
                <Kanban size={16} />
            </button>
        </Tooltip>
        <Tooltip label="Chronos Timeline">
            <button
                onClick={() => {
                    setView('chronos');
                }}
                className={`p-2 rounded-lg transition-all ${view === 'chronos' ? 'bg-cyan-500/10 text-cyan-400 shadow-inner' : 'text-weft-muted hover:text-weft'}`}
            >
                <Clock size={16} />
            </button>
        </Tooltip>
        <Tooltip label="AST Dependency Heatmap">
            <button
                onClick={() => {
                    setView('ast');
                }}
                className={`p-2 rounded-lg transition-all ${view === 'ast' ? 'bg-cyan-500/10 text-cyan-400 shadow-inner' : 'text-weft-muted hover:text-weft'}`}
            >
                <Layers size={16} />
            </button>
        </Tooltip>
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

