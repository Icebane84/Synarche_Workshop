import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
    commandRegistry,
    dispatchCommand,
    interpretNaturalLanguageCommand,
} from '../../api/SynapseBridge';
import { useSharedConsciousness } from '../../store/sharedConsciousness';
import type { CommandDefinitionGUCAv5, DispatchResult } from '../../types/synapseTypes';

import {
    BrainCircuit,
    Command,
    CornerDownLeft,
    Maximize2,
    Mic,
    Minimize2,
    Search,
    Terminal,
    X,
    RefreshCcw,
    Lock,
    Unlock,
} from 'lucide-react';
import { useNexusHandshake } from '../../../../axion-core/src/nexus';
import CommandPreview from '../Command/CommandPreview';
import CommandResultView from '../Command/CommandResultView';
import ParameterWeaver from '../Command/ParameterWeaver';
import Tooltip from '../common/Tooltip';

interface AuralInterface {
    isListening: boolean;
    transcript: string;
    startListening: () => void;
    stopListening: () => void;
    resetTranscript: () => void;
}

const useAuralInterface = (): AuralInterface => {
    // Stub for Aural Interface
    return {
        isListening: false,
        transcript: '',
        startListening: (): void => console.log('Mic stub start'),
        stopListening: (): void => console.log('Mic stub stop'),
        resetTranscript: (): void => {},
    };
};

const TheSynapse: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [query, setQuery] = useState('');
    const [selectedCommandId, setSelectedCommandId] = useState<string | null>(null);
    const [isWeaving, setIsWeaving] = useState(false);
    const [executionResult, setExecutionResult] = useState<DispatchResult | null>(null);
    const [clcMode, setClcMode] = useState(false); // Command Line Cognition Mode (Text-first)
    const [isExpanded, setIsExpanded] = useState(false);

    const inputRef = useRef<HTMLInputElement>(null);
    const listRef = useRef<HTMLDivElement>(null);

    // Audio Hooks
    const { isListening, transcript, startListening, stopListening } = useAuralInterface();

    // Store
    const cognitiveFocus = useSharedConsciousness((state) => state.cognitiveFocus);
    const addNovaSpark = useSharedConsciousness((state) => state.addNovaSpark); // NovaSparks are alerts

    // Nexus Handshake
    const { isAuthorized, nexusState, triggerSync } = useNexusHandshake();

    useEffect(() => {
        if (transcript) {
            setQuery(transcript);
        }
    }, [transcript]);

    // Global Keyboard Shortcut (Meta+K)
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent): void => {
            // Toggle Console
            if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                setIsOpen((prev) => !prev);
            }

            // Close on Escape
            if (e.key === 'Escape' && isOpen) {
                if (isWeaving) {
                    setIsWeaving(false);
                    setSelectedCommandId(null);
                } else if (executionResult) {
                    setExecutionResult(null);
                } else {
                    setIsOpen(false);
                }
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return (): void => window.removeEventListener('keydown', handleKeyDown);
    }, [isOpen, isWeaving, executionResult]);

    // Auto-focus input when opened
    useEffect(() => {
        if (isOpen && !isWeaving && !executionResult) {
            setTimeout(() => inputRef.current?.focus(), 50);
        }
    }, [isOpen, isWeaving, executionResult]);

    // Filter Commands based on query
    const filteredCommands = useMemo(() => {
        const allCommands = Object.values(commandRegistry);
        if (!query) return allCommands;
        const lowerQuery = query.toLowerCase();
        return allCommands.filter(
            (cmd) =>
                cmd.commandId.toLowerCase().includes(lowerQuery) ||
                cmd.description.toLowerCase().includes(lowerQuery) ||
                (cmd.aliases &&
                    cmd.aliases.some((alias) => alias.toLowerCase().includes(lowerQuery)))
        );
    }, [query]);

    // Handler: Select a command from list
    const handleSelectCommand = (command: CommandDefinitionGUCAv5): void => {
        setSelectedCommandId(command.commandId);
        if (command.parameters.length > 0) {
            setIsWeaving(true);
        } else {
            executeCommand(command, {});
        }
    };

    // Handler: Execute Command
    const executeCommand = async (
        command: CommandDefinitionGUCAv5,
        params: Record<string, unknown>
    ): Promise<void> => {
        try {
            const result = await dispatchCommand(command, params);
            setExecutionResult(result);

            if (result.success) {
                addNovaSpark(`Executed: ${command.commandId}`);
            } else {
                // Optional: Play error sound
            }
        } catch (error) {
            setExecutionResult({
                success: false,
                message: 'An unexpected neural dissonance occurred during execution.',
            });
            console.error(error); // Log error to console for now
        } finally {
            setIsWeaving(false);
        }
    };

    // Handler: Natural Language / CLC Input
    const handleKeyDownInput = async (e: React.KeyboardEvent): Promise<void> => {
        if (e.key === 'Enter' && query) {
            // 1. Check for exact command match (alias or ID)
            const exactMatch = Object.values(commandRegistry).find(
                (c) => c.commandId === query || c.aliases?.includes(query.toLowerCase())
            );

            if (exactMatch) {
                handleSelectCommand(exactMatch);
                return;
            }

            // 2. Try Natural Language Interpretation
            const interpretedId = await interpretNaturalLanguageCommand(query);
            if (interpretedId && commandRegistry[interpretedId]) {
                handleSelectCommand(commandRegistry[interpretedId]);
                return;
            }

            // 3. Fallback: No command found
            // In a full implementation, this might route to a chat agent
            console.log('No command found for:', query);
        }
    };

    // Render Logic
    if (!isOpen) {
        // Floating Trigger Button
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-6 right-6 p-4 bg-cyan-900/80 hover:bg-cyan-800 backdrop-blur-md rounded-full border border-cyan-500/30 text-cyan-400 shadow-[0_0_20px_rgba(34,211,238,0.2)] hover:shadow-[0_0_30px_rgba(34,211,238,0.4)] transition-all z-[9000] group"
            >
                <Terminal className="w-6 h-6 group-hover:scale-110 transition-transform" />
                <span className="absolute -top-10 left-1/2 -translate-x-1/2 bg-black/80 text-cyan-200 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                    cmd+k
                </span>
            </button>
        );
    }

    return (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
            {/* Main Console Window */}
            <div
                className={`
                relative flex flex-col bg-gray-900/95 backdrop-blur-xl border border-cyan-500/30 rounded-xl shadow-[0_0_50px_rgba(0,0,0,0.8)] overflow-hidden transition-all duration-300
                ${isExpanded ? 'w-[90vw] h-[90vh]' : 'w-full max-w-4xl h-[600px]'}
            `}
            >
                {/* Header / Input Bar */}
                <div className="flex items-center gap-4 p-4 border-b border-cyan-500/20 bg-black/20 shrink-0">
                    <div className="p-2 bg-cyan-500/10 rounded-md">
                        {clcMode ? (
                            <CornerDownLeft className="w-5 h-5 text-cyan-400" />
                        ) : (
                            <Search className="w-5 h-5 text-cyan-400" />
                        )}
                    </div>

                    <input
                        ref={inputRef}
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={handleKeyDownInput}
                        placeholder={
                            isWeaving ? 'Configuring parameters...' : 'Type a command or query...'
                        }
                        disabled={isWeaving || !!executionResult}
                        className="flex-1 bg-transparent text-lg text-cyan-100 placeholder-cyan-500/50 focus:outline-none font-light tracking-wide"
                    />

                    <div className="flex items-center gap-2">
                        <Tooltip label={isListening ? 'Stop Listening' : 'Voice Input (Beta)'}>
                            <button
                                onClick={isListening ? stopListening : startListening}
                                className={`p-2 rounded-md transition-colors ${isListening ? 'bg-red-500/20 text-red-400 animate-pulse' : 'hover:bg-cyan-500/10 text-cyan-500/60 hover:text-cyan-400'}`}
                            >
                                <Mic className="w-5 h-5" />
                            </button>
                        </Tooltip>

                        <button
                            onClick={() => setClcMode(!clcMode)}
                            className={`p-2 rounded-md transition-colors ${clcMode ? 'bg-cyan-500/20 text-cyan-300' : 'hover:bg-cyan-500/10 text-cyan-500/60 hover:text-cyan-400'}`}
                        >
                            <Terminal className="w-5 h-5" />
                        </button>

                        <div className="w-px h-6 bg-cyan-500/20 mx-1" />

                        <button
                            onClick={() => setIsExpanded(!isExpanded)}
                            className="p-2 hover:bg-cyan-500/10 rounded-md text-cyan-500/60 hover:text-cyan-400 transition-colors"
                        >
                            {isExpanded ? (
                                <Minimize2 className="w-5 h-5" />
                            ) : (
                                <Maximize2 className="w-5 h-5" />
                            )}
                        </button>

                        <button
                            onClick={() => setIsOpen(false)}
                            className="p-2 hover:bg-red-500/10 rounded-md text-cyan-500/60 hover:text-red-400 transition-colors"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                {/* Content Area */}
                <div className="flex-1 flex min-h-0">
                    {/* Mode: Execution Result */}
                    {executionResult ? (
                        <div className="w-full h-full">
                            <CommandResultView
                                result={executionResult}
                                onDone={() => {
                                    setExecutionResult(null);
                                    setQuery('');
                                    setTimeout(() => inputRef.current?.focus(), 50);
                                }}
                            />
                        </div>
                    ) : isWeaving && selectedCommandId ? (
                        /* Mode: Parameter Weaving */
                        <div className="w-full h-full bg-gradient-to-br from-gray-900 to-black/50">
                            <ParameterWeaver
                                command={commandRegistry[selectedCommandId]}
                                onSubmit={(params) =>
                                    executeCommand(commandRegistry[selectedCommandId], params)
                                }
                                onCancel={() => {
                                    setIsWeaving(false);
                                    setSelectedCommandId(null);
                                }}
                            />
                        </div>
                    ) : (
                        /* Mode: Command Selection / Search */
                        <>
                            {/* Left: Command List */}
                            <div
                                ref={listRef}
                                className={`
                                flex-1 overflow-y-auto custom-scrollbar p-2
                                ${clcMode ? 'font-mono text-sm' : ''}
                            `}
                            >
                                {filteredCommands.length > 0 ? (
                                    <div className="space-y-1">
                                        {filteredCommands.map((cmd) => (
                                            <button
                                                key={cmd.commandId}
                                                onClick={() => handleSelectCommand(cmd)}
                                                onMouseEnter={() =>
                                                    setSelectedCommandId(cmd.commandId)
                                                }
                                                className={`
                                                w-full flex items-center justify-between p-3 rounded-lg text-left transition-all group
                                                ${selectedCommandId === cmd.commandId ? 'bg-cyan-500/10 border border-cyan-500/30' : 'border border-transparent hover:bg-white/5'}
                                            `}
                                            >
                                                <div className="flex items-center gap-3">
                                                    <div
                                                        className={`p-2 rounded-md ${selectedCommandId === cmd.commandId ? 'bg-cyan-500/20 text-cyan-300' : 'bg-gray-800 text-gray-500'}`}
                                                    >
                                                        <Command className="w-4 h-4" />
                                                    </div>
                                                    <div>
                                                        <span
                                                            className={`block font-medium ${selectedCommandId === cmd.commandId ? 'text-cyan-200' : 'text-gray-400 group-hover:text-gray-200'}`}
                                                        >
                                                            {cmd.commandId}
                                                        </span>
                                                        {!clcMode && (
                                                            <span className="text-xs text-gray-500 truncate max-w-[300px]">
                                                                {cmd.description}
                                                            </span>
                                                        )}
                                                    </div>
                                                </div>

                                                {cmd.aliases && (
                                                    <div className="flex gap-1">
                                                        {cmd.aliases.map((alias) => (
                                                            <span
                                                                key={alias}
                                                                className="text-[10px] px-1.5 py-0.5 bg-black/40 rounded text-gray-500 font-mono"
                                                            >
                                                                {alias}
                                                            </span>
                                                        ))}
                                                    </div>
                                                )}
                                            </button>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="h-full flex flex-col items-center justify-center text-gray-600">
                                        <BrainCircuit className="w-12 h-12 mb-4 opacity-20" />
                                        <p>No active directives match your query.</p>
                                    </div>
                                )}
                            </div>

                            {/* Right: Preview Panel (Hidden on small screens) */}
                            <div className="hidden md:block w-[400px] border-l border-cyan-500/10 bg-black/20">
                                <CommandPreview
                                    command={
                                        selectedCommandId
                                            ? commandRegistry[selectedCommandId]
                                            : null
                                    }
                                />
                            </div>
                        </>
                    )}
                </div>

                {/* Footer */}
                <div className="p-2 border-t border-cyan-500/10 bg-black/40 text-[10px] text-cyan-500/40 flex justify-between items-center px-4">
                    <div className="flex gap-4 items-center">
                        <span>
                            COGNITIVE FOCUS:{' '}
                            <span className="text-cyan-400">{cognitiveFocus.toUpperCase()}</span>
                        </span>
                        <span>•</span>
                        <div className="flex items-center gap-1.5">
                            <span className="opacity-60">NEXUS:</span>
                            {isAuthorized ? (
                                <div className="flex items-center gap-1.5">
                                    <Unlock className="w-3 h-3 text-emerald-400" />
                                    <span className="text-emerald-400 font-mono">AUTH_ACTIVE</span>
                                    <span className="text-cyan-400/60 ml-2">SYNC:{nexusState.syncCount}</span>
                                    <button 
                                        onClick={triggerSync}
                                        className="ml-1 p-1 hover:bg-cyan-500/10 rounded transition-colors group"
                                        title="Trigger Nexus Sync"
                                    >
                                        <RefreshCcw className="w-3 h-3 text-cyan-400 group-active:rotate-180 transition-transform" />
                                    </button>
                                </div>
                            ) : (
                                <div className="flex items-center gap-1.5">
                                    <Lock className="w-3 h-3 text-red-400" />
                                    <span className="text-red-400 font-mono animate-pulse">AUTH_REQUIRED</span>
                                </div>
                            )}
                        </div>
                    </div>
                    <div className="font-mono flex items-center gap-3">
                        <span>DISSONANCE: <span className="text-cyan-400">LOW</span></span>
                        <span className="opacity-20">|</span>
                        <span>GUCA v5.0 // SYNARCHY BRIDGE ACTIVE</span>
                    </div>
                </div>

                <style>{`
                .custom-scrollbar::-webkit-scrollbar { width: 6px; }
                .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(34, 211, 238, 0.1); border-radius: 3px; }
                .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(34, 211, 238, 0.3); }
                @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
                .animate-fade-in { animation: fade-in 0.2s ease-out; }
            `}</style>
            </div>
        </div>
    );
};

export default TheSynapse;
