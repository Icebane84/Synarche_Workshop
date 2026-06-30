import { motion, AnimatePresence } from 'framer-motion';
import { 
    AlertOctagon, 
    ArrowDown, 
    ArrowUp, 
    CheckCircle, 
    Copy, 
    FileText, 
    Lightbulb, 
    Link as LinkIcon, 
    Minus, 
    Sparkles, 
    User,
    Loader
} from 'lucide-react';
import React, { useState } from 'react';
import { useTaskStore } from '../../store/taskStore';
import { useFileSystemStore } from '../../store/fileSystemStore';
import { Task, TaskPriority, TaskSource, TaskStatus } from '@essence/types';
import Tooltip from '../common/Tooltip';

/**
 * TaskCard Component [OMEGA v15.0]
 * Modularized unit of work (Thought Weft).
 */

const sourceMetadata: Record<
    TaskSource,
    { icon: React.ComponentType<{ className?: string; size?: number }>; color: string; label: string }
> = {
    Manual: { icon: User, color: 'cyan', label: 'Manual Input' },
    'Dissonance Scanner': { icon: AlertOctagon, color: 'amber', label: 'Dissonance Scanner' },
    'Synergy Simulator': { icon: Lightbulb, color: 'emerald', label: 'Synergy Simulator' },
    'Neural Link': { icon: LinkIcon, color: 'indigo', label: 'Neural Link' },
};

const priorityMetadata: Record<
    TaskPriority,
    { icon: React.ComponentType<{ className?: string; size?: number }>; color: string; label: string }
> = {
    Low: { icon: ArrowDown, color: 'sky', label: 'Low Priority' },
    Medium: { icon: Minus, color: 'gray', label: 'Medium Priority' },
    High: { icon: ArrowUp, color: 'red', label: 'High Priority' },
};

interface TaskCardProps {
    task: Task;
    onSelect: () => void;
    onStatusChange?: (status: TaskStatus) => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task, onSelect, onStatusChange }) => {
    const sourceMeta = sourceMetadata[task.source];
    const priorityMeta = priorityMetadata[task.priority];
    
    const [copied, setCopied] = useState(false);
    const [isRepairing, setIsRepairing] = useState(false);
    
    const resolveDissonance = useTaskStore((state) => state.resolveDissonance);
    const isNeuralLinkActive = useFileSystemStore((state) => state.isConnected);

    const handleDragStart = (e: React.DragEvent<HTMLDivElement>) => {
        e.dataTransfer.setData('taskId', task.id);
    };

    const handleCopy = (e: React.MouseEvent) => {
        e.stopPropagation();
        const text = `[${task.id}] ${task.title}\n\n${task.notes ?? 'No notes.'}`;
        void navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => { setCopied(false); }, 2000);
    };

    const handleStatusAction = (e: React.MouseEvent, newStatus: TaskStatus) => {
        e.stopPropagation();
        onStatusChange?.(newStatus);
    };

    const handleRepair = async (e: React.MouseEvent) => {
        e.stopPropagation();
        if (!isNeuralLinkActive) return;

        setIsRepairing(true);
        try {
            const result = await resolveDissonance(task.id);
            if (!result.success) {
                alert(`Repair Failed: ${result.message}`);
            }
        } finally {
            setIsRepairing(false);
        }
    };

    const handleRepairAction = (e: React.MouseEvent): void => {
        void handleRepair(e);
    };

    // Derived style for priority indicator
    let priorityColor = 'var(--color-resonant-accent)';
    if (priorityMeta.color === 'red') {
        priorityColor = 'var(--color-resonant-error)';
    } else if (priorityMeta.color === 'amber') {
        priorityColor = 'var(--color-resonant-warning)';
    }

    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            whileHover={{ scale: 1.02 }}
            draggable={!isRepairing}
            onDragStart={(e) => handleDragStart(e as unknown as React.DragEvent<HTMLDivElement>)}
            onClick={onSelect}
            className={`group relative p-4 glass-panel cursor-pointer hover:border-cyan-400/30 transition-all duration-300 ${isRepairing ? 'opacity-70 pointer-events-none' : ''}`}
        >
            {/* Priority Indicator */}
            <div 
                className="absolute left-0 top-0 bottom-0 w-1 rounded-l-lg opacity-80" 
                style={{ backgroundColor: priorityColor }}
            />

            <div className="pl-2">
                <div className="flex justify-between items-start gap-4">
                    <div className="space-y-1">
                        <p className="text-weft font-medium text-sm leading-tight group-hover:text-cyan-200 transition-colors">
                            {task.title}
                        </p>
                        {isRepairing && (
                            <div className="flex items-center gap-1.5 text-[8px] font-mono text-amber-500 uppercase tracking-widest animate-pulse">
                                <Loader size={8} className="animate-spin" />
                                Repairing Substrate...
                            </div>
                        )}
                    </div>
                    
                    <div className="flex items-center gap-1.5">
                        <AnimatePresence>
                            {task.source === 'Dissonance Scanner' && task.status === 'To Do' && (
                                <Tooltip label={isNeuralLinkActive ? "Code Smith: Repair Dissonance" : "Neural Link Required for Repair"}>
                                    <button
                                        onClick={handleRepairAction}
                                        disabled={!isNeuralLinkActive || isRepairing}
                                        className={`p-1 px-1.5 rounded transition-all flex items-center gap-1 ${
                                            isNeuralLinkActive 
                                                ? 'bg-amber-500/20 text-amber-500 hover:bg-amber-500/30' 
                                                : 'bg-gray-500/10 text-gray-500/50 cursor-not-allowed opacity-50'
                                        }`}
                                    >
                                        <Sparkles size={14} className={isRepairing ? "animate-spin" : "animate-pulse"} />
                                    </button>
                                </Tooltip>
                            )}

                            {!isRepairing && task.status === 'To Do' && (
                                <Tooltip label="Start Sense">
                                    <button
                                        onClick={(e) => { handleStatusAction(e, 'In Progress'); }}
                                        className="p-1 px-1.5 rounded bg-cyan-400/10 text-cyan-400 opacity-0 group-hover:opacity-100 transition-all"
                                    >
                                        <div className="w-1.5 h-1.5 bg-current rounded-full animate-pulse" />
                                    </button>
                                </Tooltip>
                            )}
                            
                            {!isRepairing && task.status === 'In Progress' && (
                                <Tooltip label="Anchor Task">
                                    <button
                                        onClick={(e) => { handleStatusAction(e, 'Completed'); }}
                                        className="p-1 rounded hover:bg-emerald-500/20 text-gray-500 hover:text-emerald-400 transition-colors opacity-0 group-hover:opacity-100"
                                    >
                                        <CheckCircle size={14} />
                                    </button>
                                </Tooltip>
                            )}
                        </AnimatePresence>

                        <button
                            onClick={handleCopy}
                            className={`p-1 rounded hover:bg-white/5 transition-colors ${copied ? 'text-emerald-400' : 'text-gray-600 opacity-0 group-hover:opacity-100'}`}
                        >
                            <Copy size={12} />
                        </button>
                    </div>
                </div>

                <div className="flex items-center justify-between mt-4 text-[10px] font-mono tracking-wider">
                    <div className="flex items-center gap-2 text-weft-muted">
                        <sourceMeta.icon size={12} />
                        <span className="uppercase">{task.source}</span>
                    </div>
                    {task.notes && (
                      <div className="text-cyan-500/40">
                        <FileText size={12} />
                      </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};
