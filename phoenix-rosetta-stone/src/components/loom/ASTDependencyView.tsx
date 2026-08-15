import React, { useState } from 'react';
import { AlertCircle, CheckCircle2, FileCode, Play, ShieldAlert, Sparkles, Wrench } from 'lucide-react';
import { useTaskStore } from '../../store/taskStore';
import { useFileSystemStore } from '../../store/fileSystemStore';
import { resolveDissonance } from '../../services/repairService';

export const ASTDependencyView: React.FC = () => {
    const tasks = useTaskStore((state) => state.tasks);
    const scannedFiles = useFileSystemStore((state) => state.scannedFiles);
    const [repairingId, setRepairingId] = useState<string | null>(null);
    const [filter, setFilter] = useState<'All' | 'High' | 'Clean'>('All');

    // Group tasks by file
    const fileHealthMap = scannedFiles.map((file) => {
        const fileTasks = tasks.filter(
            (t) => t.notes?.includes(file.path) && t.status !== 'Completed'
        );
        const hasHigh = fileTasks.some((t) => t.priority === 'High');
        const isClean = fileTasks.length === 0;

        return {
            file,
            tasks: fileTasks,
            hasHigh,
            isClean,
        };
    });

    const filteredFiles = fileHealthMap.filter((item) => {
        if (filter === 'High') return item.hasHigh;
        if (filter === 'Clean') return item.isClean;
        return true;
    });

    const handleRepair = async (taskId: string) => {
        setRepairingId(taskId);
        try {
            await resolveDissonance(taskId);
        } finally {
            setRepairingId(null);
        }
    };

    return (
        <div className="space-y-4">
            {/* Filter Tabs */}
            <div className="flex items-center justify-between bg-black/40 border border-cyan-900/40 p-3 rounded-lg backdrop-blur-sm">
                <div className="flex items-center gap-2">
                    <span className="text-xs uppercase tracking-widest text-cyan-400 font-mono">AST Health Filter:</span>
                    {(['All', 'High', 'Clean'] as const).map((mode) => (
                        <button
                            key={mode}
                            onClick={() => setFilter(mode)}
                            className={`px-3 py-1 text-xs rounded transition-all font-mono ${
                                filter === mode
                                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/50 shadow-[0_0_10px_rgba(6,182,212,0.3)]'
                                    : 'text-slate-400 hover:text-cyan-200 hover:bg-cyan-950/30'
                            }`}
                        >
                            {mode === 'High' ? '🔴 Critical' : mode === 'Clean' ? '🟢 Clean' : '⚪ All Files'}
                        </button>
                    ))}
                </div>
                <div className="text-xs font-mono text-slate-400">
                    Showing <span className="text-cyan-300 font-bold">{filteredFiles.length}</span> of {scannedFiles.length} files
                </div>
            </div>

            {/* File Health Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {filteredFiles.map(({ file, tasks: fileTasks, hasHigh, isClean }, idx) => (
                    <div
                        key={file.path || file.name || `ast-file-${idx}`}
                        className={`p-3 rounded-lg border transition-all ${
                            isClean
                                ? 'bg-slate-950/40 border-emerald-900/30 hover:border-emerald-500/40'
                                : hasHigh
                                ? 'bg-red-950/20 border-red-800/40 hover:border-red-500/60 shadow-[0_0_12px_rgba(239,68,68,0.1)]'
                                : 'bg-amber-950/20 border-amber-800/40 hover:border-amber-500/50'
                        }`}
                    >
                        <div className="flex items-start justify-between gap-2">
                            <div className="flex items-center gap-2 min-w-0">
                                <FileCode className={`w-4 h-4 shrink-0 ${isClean ? 'text-emerald-400' : hasHigh ? 'text-red-400' : 'text-amber-400'}`} />
                                <span className="text-xs font-mono font-medium text-slate-200 truncate" title={file.name}>
                                    {file.name}
                                </span>
                            </div>
                            <span
                                className={`text-[10px] uppercase font-mono px-1.5 py-0.5 rounded shrink-0 ${
                                    isClean
                                        ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/50'
                                        : hasHigh
                                        ? 'bg-red-950 text-red-300 border border-red-800/60 font-bold'
                                        : 'bg-amber-950 text-amber-300 border border-amber-800/50'
                                }`}
                            >
                                {isClean ? 'Resonant' : `${fileTasks.length} ${fileTasks.length === 1 ? 'Dissonance' : 'Dissonances'}`}
                            </span>
                        </div>

                        <div className="mt-2 text-[11px] font-mono text-slate-400 truncate" title={file.path}>
                            {file.path}
                        </div>

                        {!isClean && fileTasks.length > 0 && (
                            <div className="mt-3 pt-2 border-t border-slate-800/60 flex items-center justify-between">
                                <span className="text-[10px] text-slate-400 font-mono">
                                    Priority: <span className={hasHigh ? 'text-red-400 font-bold' : 'text-amber-400'}>{hasHigh ? 'High' : 'Medium'}</span>
                                </span>
                                <button
                                    onClick={() => handleRepair(fileTasks[0].id)}
                                    disabled={repairingId === fileTasks[0].id}
                                    className="flex items-center gap-1 px-2.5 py-1 text-[11px] font-mono rounded bg-cyan-950 hover:bg-cyan-900/60 text-cyan-300 border border-cyan-700/50 transition-all disabled:opacity-50"
                                >
                                    {repairingId === fileTasks[0].id ? (
                                        <>
                                            <Wrench className="w-3 h-3 animate-spin text-cyan-400" />
                                            <span>Repairing...</span>
                                        </>
                                    ) : (
                                        <>
                                            <Sparkles className="w-3 h-3 text-cyan-400" />
                                            <span>Heal File</span>
                                        </>
                                    )}
                                </button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};
