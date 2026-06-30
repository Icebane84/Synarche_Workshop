import React from 'react';
import { Trash2, ChevronDown } from 'lucide-react';
import { Task, TaskStatus } from '@essence/types';
import { TaskCard } from './TaskCard';
import Tooltip from '../common/Tooltip';
import { AnimatePresence, motion } from 'framer-motion';

/**
 * KanbanColumn Component [OMEGA v15.0]
 * Handles the logic for a single task column (To Do, In Progress, Completed).
 */

interface KanbanColumnProps {
    status: TaskStatus;
    tasks: Task[];
    visibleCount: number;
    onSelectTask: (taskId: string) => void;
    onStatusChange: (taskId: string, newStatus: TaskStatus) => void;
    onLoadMore: () => void;
    onClearCompleted?: () => void;
    onDrop: (e: React.DragEvent<HTMLDivElement>, status: TaskStatus) => void;
}

export const KanbanColumn: React.FC<KanbanColumnProps> = ({
    status,
    tasks,
    visibleCount,
    onSelectTask,
    onStatusChange,
    onLoadMore,
    onClearCompleted,
    onDrop,
}) => {
    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.currentTarget.classList.add('bg-cyan-500/5', 'border-cyan-500/20');
    };

    const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
        e.currentTarget.classList.remove('bg-cyan-500/5', 'border-cyan-500/20');
    };

    return (
        <div
            onDrop={(e) => {
                e.currentTarget.classList.remove('bg-cyan-500/5', 'border-cyan-500/20');
                onDrop(e, status);
            }}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className="flex flex-col bg-black/40 border border-cyan-500/5 rounded-xl p-4 transition-all duration-300 min-h-[500px]"
        >
            <h3 className="text-sm font-bold tracking-widest text-cyan-400 uppercase mb-6 pb-2 border-b border-cyan-500/10 flex justify-between items-center shrink-0">
                <span>{status}</span>
                <div className="flex items-center gap-3">
                    <span className="text-[10px] font-mono opacity-40">{tasks.length}</span>
                    {status === 'Completed' && tasks.length > 0 && onClearCompleted && (
                        <Tooltip label="Eradicate Completed Wefts">
                            <button
                                onClick={onClearCompleted}
                                className="p-1 hover:bg-red-500/10 text-red-500/30 hover:text-red-400 rounded transition-all"
                            >
                                <Trash2 size={14} />
                            </button>
                        </Tooltip>
                    )}
                </div>
            </h3>

            <div className="flex-1 overflow-y-auto space-y-4 pr-1 custom-scrollbar min-h-0">
                {tasks.length > 0 ? (
                    <AnimatePresence mode="popLayout">
                        {tasks.slice(0, visibleCount).map((task) => (
                            <TaskCard
                                key={task.id}
                                task={task}
                                onSelect={() => { onSelectTask(task.id); }}
                                onStatusChange={(newStatus) => { onStatusChange(task.id, newStatus); }}
                            />
                        ))}
                    </AnimatePresence>
                ) : (
                    <div className="h-full flex items-center justify-center text-weft-muted text-[10px] uppercase tracking-tighter opacity-20">
                        EMPTY TAPESTRY
                    </div>
                )}

                {tasks.length > visibleCount && (
                    <motion.button
                        whileHover={{ scale: 1.01 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={onLoadMore}
                        className="w-full py-4 mt-6 bg-cyan-500/5 border border-cyan-500/10 rounded-lg text-cyan-400 text-[10px] font-mono flex items-center justify-center gap-2 hover:bg-cyan-500/10 transition-all uppercase tracking-[0.2em]"
                    >
                        <ChevronDown size={14} /> EXPAND VIEW (+50)
                    </motion.button>
                )}
            </div>
        </div>
    );
};
