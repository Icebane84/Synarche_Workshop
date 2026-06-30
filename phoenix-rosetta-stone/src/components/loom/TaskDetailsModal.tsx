import React, { useState } from 'react';
import { 
    X, 
    Copy, 
    CheckCircle, 
    FileText, 
    Save, 
    Loader,
    User,
    AlertOctagon,
    Lightbulb,
    Link as LinkIcon,
    ArrowDown,
    Minus,
    ArrowUp
} from 'lucide-react';
import { Task, TaskPriority, TaskSource } from '@essence/types';
import Tooltip from '../common/Tooltip';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * TaskDetailsModal Component [OMEGA v15.0]
 * High-fidelity inspection of a specific Thought Weft.
 */

const sourceMetadata: Record<
    TaskSource,
    { icon: React.ComponentType<{ className?: string }>; color: string; label: string }
> = {
    Manual: { icon: User, color: 'cyan', label: 'Manual Input' },
    'Dissonance Scanner': { icon: AlertOctagon, color: 'amber', label: 'Dissonance Scanner' },
    'Synergy Simulator': { icon: Lightbulb, color: 'emerald', label: 'Synergy Simulator' },
    'Neural Link': { icon: LinkIcon, color: 'indigo', label: 'Neural Link' },
};

const priorityMetadata: Record<
    TaskPriority,
    { icon: React.ComponentType<{ className?: string }>; color: string; label: string }
> = {
    Low: { icon: ArrowDown, color: 'sky', label: 'Low Priority' },
    Medium: { icon: Minus, color: 'gray', label: 'Medium Priority' },
    High: { icon: ArrowUp, color: 'red', label: 'High Priority' },
};

interface TaskDetailsModalProps {
    task: Task;
    onClose: () => void;
    onUpdateNotes: (taskId: string, notes: string) => Promise<void>;
}

export const TaskDetailsModal: React.FC<TaskDetailsModalProps> = ({ task, onClose, onUpdateNotes }) => {
    const [notes, setNotes] = useState(task.notes);
    const [isSaving, setIsSaving] = useState(false);
    const [copied, setCopied] = useState(false);

    const sourceMeta = sourceMetadata[task.source];
    const priorityMeta = priorityMetadata[task.priority];
    const hasChanged = notes !== task.notes;

    const handleSave = async () => {
        if (!hasChanged) return;
        setIsSaving(true);
        await onUpdateNotes(task.id, notes);
        setIsSaving(false);
        onClose();
    };

    const handleCopy = () => {
        const text = `[${task.id}] ${task.title}\n\n${notes || 'No notes.'}`;
        void navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => { setCopied(false); }, 2000);
    };

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4"
                onClick={onClose}
            >
                <motion.div
                    initial={{ scale: 0.95, opacity: 0, y: 20 }}
                    animate={{ scale: 1, opacity: 1, y: 0 }}
                    exit={{ scale: 0.95, opacity: 0, y: 20 }}
                    onClick={(e) => { e.stopPropagation(); }}
                    className="relative w-full max-w-xl glass-panel p-8 shadow-2xl flex flex-col max-h-[85vh] border-cyan-500/20"
                >
                    {/* Header Controls */}
                    <div className="absolute top-6 right-6 flex items-center gap-4">
                        <button
                            onClick={handleCopy}
                            className={`p-2 rounded-lg hover:bg-white/5 transition-all ${copied ? 'text-emerald-400' : 'text-weft-muted'}`}
                        >
                            {copied ? <CheckCircle size={18} /> : <Copy size={18} />}
                        </button>
                        <button
                            onClick={onClose}
                            className="p-2 rounded-lg hover:bg-red-500/10 text-weft-muted hover:text-red-400 transition-all"
                        >
                            <X size={20} />
                        </button>
                    </div>

                    <h3 className="text-3xl font-thin tracking-tight text-white mb-2 pr-12 line-clamp-2">
                        {task.title}
                    </h3>

                    <div className="flex items-center gap-4 text-[10px] font-mono text-cyan-500/50 mb-8 tracking-widest uppercase">
                        <span>NODE ID: {task.id}</span>
                        <span>|</span>
                        <span>ANCHOR: {new Date(task.timestamp).toLocaleString()}</span>
                    </div>

                    {/* Metadata Grid */}
                    <div className="grid grid-cols-2 gap-4 mb-8">
                        <div className="p-4 bg-void-muted/50 rounded-xl border border-white/5 flex items-center gap-4">
                            <div className={`p-3 rounded-xl bg-${sourceMeta.color}-500/10`}>
                                <sourceMeta.icon className={`w-5 h-5 text-${sourceMeta.color}-400`} />
                            </div>
                            <div>
                                <p className="text-[10px] uppercase font-bold tracking-widest text-weft-muted opacity-40">Source</p>
                                <p className="text-sm font-medium tracking-wide">{sourceMeta.label}</p>
                            </div>
                        </div>
                        <div className="p-4 bg-void-muted/50 rounded-xl border border-white/5 flex items-center gap-4">
                            <div className={`p-3 rounded-xl bg-${priorityMeta.color}-500/10`}>
                                <priorityMeta.icon className={`w-5 h-5 text-${priorityMeta.color}-400`} />
                            </div>
                            <div>
                                <p className="text-[10px] uppercase font-bold tracking-widest text-weft-muted opacity-40">Priority</p>
                                <p className="text-sm font-medium tracking-wide">{priorityMeta.label}</p>
                            </div>
                        </div>
                    </div>

                    {/* Notes Area */}
                    <div className="flex-1 flex flex-col min-h-0 bg-void/30 p-6 rounded-2xl border border-white/5">
                        <label className="text-[10px] font-bold uppercase tracking-widest text-cyan-400 mb-4 flex items-center gap-2 opacity-60">
                            <FileText size={12} /> Observations
                        </label>
                        <textarea
                            value={notes}
                            onChange={(e) => { setNotes(e.target.value); }}
                            placeholder="Infuse detailed notes..."
                            className="bg-transparent text-sm text-weft leading-relaxed w-full flex-1 resize-none focus:outline-none custom-scrollbar"
                        />
                    </div>

                    {/* Footer Actions */}
                    <div className="mt-8 flex justify-end">
                        <motion.button
                            whileHover={hasChanged ? { scale: 1.02 } : {}}
                            whileTap={hasChanged ? { scale: 0.98 } : {}}
                            onClick={() => void handleSave()}
                            disabled={isSaving || !hasChanged}
                            className={`flex items-center gap-3 px-8 py-3 rounded-xl text-sm font-bold tracking-widest uppercase transition-all ${
                                hasChanged
                                    ? 'bg-cyan-500/20 text-cyan-200 border border-cyan-400/50 shadow-xl'
                                    : 'bg-white/5 text-weft-muted cursor-not-allowed border border-white/5'
                            }`}
                        >
                            {isSaving ? (
                              <>
                                <Loader size={16} className="animate-spin" /> Transmitting...
                              </>
                            ) : (
                              <>
                                <Save size={16} /> Anchor Changes
                              </>
                            )}
                        </motion.button>
                    </div>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};
