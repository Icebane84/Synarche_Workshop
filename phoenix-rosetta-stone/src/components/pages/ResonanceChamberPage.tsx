import React, { useState, useEffect, useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { useCoherenceStore } from '../../store/coherenceStore';
import { pathCommandMap, focusCommandMap, clearResonanceData, getResonanceState } from '../../services';
import { ScoredCommand } from '@essence/types';
import { Zap, Signal, Lightbulb, Trash2, Link, Target, Hash, Clock } from 'lucide-react';
import Tooltip from '../common/Tooltip';

const ResonanceChamberPage: React.FC = () => {
    const location = useLocation();
    const cognitiveFocus = useCoherenceStore((state) => state.cognitiveFocus);
    const [resonanceState, setResonanceState] = useState<ScoredCommand[]>(getResonanceState());

    useEffect(() => {
        const updateState = () => {
            setResonanceState(getResonanceState());
        };
        globalThis.addEventListener('storage', updateState);
        window.addEventListener('focus', updateState);

        const customEventHandler = () => {
            updateState();
        };
        globalThis.addEventListener('resonance-cleared', customEventHandler);

        return () => {
            globalThis.removeEventListener('storage', updateState);
            window.removeEventListener('focus', updateState);
            globalThis.removeEventListener('resonance-cleared', customEventHandler);
        };
    }, []);

    const handleClearResonance = () => {
        clearResonanceData();
        globalThis.dispatchEvent(new CustomEvent('resonance-cleared'));
    };

    const maxScore = useMemo(() => Math.max(...resonanceState.map((c) => c.score), 0) || 1, [resonanceState]);

    const activePathEchoes = pathCommandMap[location.pathname] ?? [];
    const activeFocusEchoes = focusCommandMap[cognitiveFocus] ?? [];
    const allEchoCommands = [...new Set([...activePathEchoes, ...activeFocusEchoes])];

    return (
        <div className="min-h-full w-full p-4 md:p-6 flex flex-col items-center">
            <div className="w-full max-w-6xl text-center mb-8">
                <h2 className="text-3xl font-thin tracking-widest text-cyan-300 drop-shadow-[0_0_8px_rgba(100,220,255,0.7)] mb-2 flex items-center justify-center gap-3">
                    <Signal className="w-8 h-8" /> Resonance Chamber
                </h2>
                <p className="text-cyan-400/80 max-w-3xl mx-auto">
                    A diagnostic visualization of the contextual systems that power The Synapse. Observe how the AI
                    prioritizes commands based on context (Cognitive Echo) and usage patterns (Resonance).
                </p>
            </div>

            <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Cognitive Echo Column */}
                <div className="p-4 bg-black/30 border border-cyan-500/10 rounded-lg flex flex-col">
                    <h3 className="text-xl font-light tracking-wider text-cyan-200 drop-shadow-lg mb-4 flex items-center gap-2">
                        <Lightbulb className="text-amber-400" /> Cognitive Echo
                    </h3>
                    <div className="p-3 bg-gray-900/40 border border-gray-700 rounded-md mb-4">
                        <p className="text-sm text-cyan-300/80">Current Context:</p>
                        <div className="flex items-center gap-4 mt-1 text-xs">
                            <div className="flex items-center gap-1.5">
                                <Link size={14} className="text-cyan-400" /> Path:{' '}
                                <span className="font-mono text-cyan-200">{location.pathname}</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                                <Target size={14} className="text-cyan-400" /> Focus:{' '}
                                <span className="font-mono text-cyan-200">{cognitiveFocus}</span>
                            </div>
                        </div>
                    </div>

                    <div className="flex-1 overflow-y-auto pr-2 space-y-4 scrollbar-thin">
                        <div>
                            <h4 className="text-md text-cyan-300 mb-2">Path-Based Echoes</h4>
                            {Object.entries(pathCommandMap).map(([path, commands]) => (
                                <div
                                    key={path}
                                    className={`p-2 rounded-md transition-colors ${
                                        location.pathname === path ? 'bg-cyan-500/10' : 'opacity-60'
                                    }`}
                                >
                                    <p className="font-mono text-xs text-cyan-400">
                                        {path} <span className="text-cyan-400/60">-&gt;</span>
                                    </p>
                                    <ul className="pl-4">
                                        {commands?.map((cmdId) => (
                                            <li key={cmdId} className="text-sm text-cyan-200 font-medium">
                                                {cmdId}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            ))}
                        </div>
                        <div>
                            <h4 className="text-md text-cyan-300 mb-2">Focus-Based Echoes</h4>
                            {Object.entries(focusCommandMap).map(([focus, commands]) => (
                                <div
                                    key={focus}
                                    className={`p-2 rounded-md transition-colors ${
                                        cognitiveFocus === focus ? 'bg-cyan-500/10' : 'opacity-60'
                                    }`}
                                >
                                    <p className="font-mono text-xs text-cyan-400">
                                        {focus} <span className="text-cyan-400/60">-&gt;</span>
                                    </p>
                                    <ul className="pl-4">
                                        {commands.map((cmdId) => (
                                            <li key={cmdId} className="text-sm text-cyan-200 font-medium">
                                                {cmdId}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-cyan-500/10">
                        <h4 className="text-md text-cyan-300 mb-2">Resulting Echoes for Current Context</h4>
                        {allEchoCommands.length > 0 ? (
                            <div className="flex flex-wrap gap-2">
                                {allEchoCommands.map((cmdId) => (
                                    <span
                                        key={cmdId}
                                        className="bg-amber-900/50 text-amber-200 text-xs font-semibold px-2 py-1 rounded-full border border-amber-500/30 flex items-center gap-1"
                                    >
                                        <Lightbulb size={10} className="text-amber-200" /> {cmdId}
                                    </span>
                                ))}
                            </div>
                        ) : (
                            <p className="text-sm text-cyan-400/60 italic">No specific echoes for this context.</p>
                        )}
                    </div>
                </div>

                {/* Command Resonance Column */}
                <div className="p-4 bg-black/30 border border-cyan-500/10 rounded-lg flex flex-col h-[600px]">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xl font-light tracking-wider text-cyan-200 drop-shadow-lg flex items-center gap-2">
                            <Zap className="text-indigo-400" /> Command Resonance
                        </h3>
                        <Tooltip label="Clear all command usage history from this browser.">
                            <button
                                onClick={handleClearResonance}
                                className="flex items-center gap-1.5 text-xs text-cyan-400/60 hover:text-red-400 transition-colors"
                            >
                                <Trash2 size={14} /> Clear History
                            </button>
                        </Tooltip>
                    </div>

                    <div className="flex-1 overflow-y-auto pr-2 scrollbar-thin space-y-3">
                        {resonanceState.map((item, index) => {
                            const { command, score, usage } = item;
                            const isEcho = allEchoCommands.includes(command.commandId);

                            return (
                                <div
                                    key={command.commandId}
                                    className={`p-4 border-l-4 rounded-r-lg transition-all duration-300 animate-fade-in-up ${
                                        isEcho
                                            ? 'bg-amber-900/10 border-l-amber-500 border-y border-r border-amber-500/20 shadow-[0_0_15px_rgba(245,158,11,0.1)]'
                                            : 'bg-gray-900/40 border-l-indigo-500 border-y border-r border-cyan-500/10 hover:border-indigo-400/30 hover:bg-gray-900/60'
                                    }`}
                                    style={{ animationDelay: `${Math.min(index * 50, 500).toString()}ms` }}
                                >
                                    <div className="flex justify-between items-start mb-2">
                                        <div className="flex-1 min-w-0 mr-4">
                                            <div className="flex items-center gap-2 mb-2">
                                                <span
                                                    className={`font-semibold tracking-wide truncate ${
                                                        isEcho ? 'text-amber-200' : 'text-cyan-100'
                                                    }`}
                                                >
                                                    {command.commandId}
                                                </span>
                                                {isEcho && (
                                                    <span className="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 text-[10px] font-bold uppercase tracking-widest border border-amber-500/30 flex items-center gap-1 shrink-0">
                                                        <Lightbulb size={10} className="animate-pulse" /> Echo Active
                                                    </span>
                                                )}
                                            </div>

                                            <p className="text-xs text-cyan-400/70 mb-3 line-clamp-2">
                                                {command.description}
                                            </p>

                                            {usage ? (
                                                <div className="flex flex-wrap items-center gap-3 text-xs">
                                                    <div className="flex items-center gap-1.5 bg-black/40 border border-cyan-500/20 px-2 py-1 rounded text-cyan-200">
                                                        <Hash size={12} className="text-cyan-500" />
                                                        <span className="font-mono">{usage.count}</span> Executions
                                                    </div>
                                                    <div className="flex items-center gap-1.5 bg-black/40 border border-cyan-500/20 px-2 py-1 rounded text-cyan-200">
                                                        <Clock size={12} className="text-cyan-500" />
                                                        <span className="font-mono">
                                                            {new Date(usage.lastUsed).toLocaleTimeString([], {
                                                                hour: '2-digit',
                                                                minute: '2-digit',
                                                            })}
                                                        </span>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="text-xs text-gray-500 italic flex items-center gap-1">
                                                    <Hash size={12} /> No usage data
                                                </div>
                                            )}
                                        </div>
                                        <div className="text-right shrink-0 flex flex-col items-end">
                                            <div
                                                className={`text-3xl font-mono font-bold leading-none drop-shadow-lg ${
                                                    isEcho ? 'text-amber-400' : 'text-indigo-400'
                                                }`}
                                            >
                                                {score.toFixed(2)}
                                            </div>
                                            <div
                                                className={`text-[9px] uppercase tracking-widest mt-1 ${
                                                    isEcho ? 'text-amber-500/60' : 'text-indigo-400/60'
                                                }`}
                                            >
                                                Resonance Score
                                            </div>
                                        </div>
                                    </div>

                                    <div className="relative w-full h-1.5 bg-gray-800 rounded-full overflow-hidden mt-3">
                                        <div
                                            className={`absolute top-0 left-0 h-full rounded-full transition-all duration-700 ${
                                                isEcho
                                                    ? 'bg-gradient-to-r from-amber-600 to-amber-400'
                                                    : 'bg-gradient-to-r from-indigo-600 to-cyan-400'
                                            }`}
                                            style={{ width: `${((score / maxScore) * 100).toString()}%` }}
                                        ></div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
            <style>{`
                .scrollbar-thin::-webkit-scrollbar { width: 4px; }
                .scrollbar-thin::-webkit-scrollbar-track { background: transparent; }
                .scrollbar-thin::-webkit-scrollbar-thumb { background-color: rgba(0, 255, 255, 0.2); border-radius: 20px; }
                 @keyframes fade-in-up {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-fade-in-up { 
                    animation: fade-in-up 0.4s ease-out forwards;
                    opacity: 0;
                }
            `}</style>
        </div>
    );
};

export default ResonanceChamberPage;

