/**
 * Core Logic: src/hooks/useSynapseLogic.ts
 * Visual Interface: src/components/TheSynapse.tsx (now exporting SynapseInterface)
 * Superposition Demo: src/components/pages/ArtifactCatalogPage.tsx (Neural Assistant)
 */
import {
    ArrowRight,
    Image as ImageIcon,
    Lightbulb,
    ListPlus,
    Loader,
    Mic,
    MicOff,
    Play,
    Search,
    Trash2,
} from 'lucide-react';
import React, { useRef } from 'react';
import { useAuralInterface } from '../hooks/useAuralInterface';
import { useTheme } from '../hooks/useTheme';
import {
    commandRegistry,
    dispatchCommand as globalDispatch,
    trackCommandExecution,
} from '../services';
import { CommandDefinitionGUCAv5 } from '@essence/codex';
import { useCoherenceStore } from '../store/coherenceStore';
import { DispatchResult, WeaverValue } from '@essence/types';
import CommandPreview from './CommandPreview';
import CommandResultView from './CommandResultView';
import Tooltip from './common/Tooltip';
import ParameterWeaver from './ParameterWeaver';
import { useSynapseLogic, CommandWithMetadata } from '../hooks/useSynapseLogic';

interface SynapseInterfaceProps {
    registry?: Record<string, CommandDefinitionGUCAv5>;
    dispatcher?: (command: CommandDefinitionGUCAv5, params: Record<string, any>) => Promise<DispatchResult>;
    onClose: () => void;
    onNovaSpark?: (message: string) => void;
    isGlobal?: boolean;
}

/**
 * The decoupled core interface of the Synapse.
 * Can be embedded inline or inside a portal.
 */
export const SynapseInterface: React.FC<SynapseInterfaceProps> = ({
    registry = commandRegistry,
    dispatcher = globalDispatch,
    onClose,
    onNovaSpark,
    isGlobal = false
}) => {
    const theme = useTheme();
    const inputRef = useRef<HTMLInputElement>(null);
    const cognitiveFocus = useCoherenceStore((state) => state.cognitiveFocus);

    const { state, actions } = useSynapseLogic({
        registry,
        dispatchCommand: dispatcher,
        onNovaSpark,
        cognitiveFocus,
        isGlobal
    });

    const {
        searchQuery,
        selectedIndex,
        confirmationCandidate,
        commandForParams,
        isClcMode,
        currentConstruction,
        isFiring,
        commandResult,
        visualContext,
        filteredCommands,
        isListening
    } = state;

    const {
        setSearchQuery,
        setSelectedIndex,
        setConfirmationCandidate,
        setCommandForParams,
        setVisualContext,
        setCurrentConstruction,
        resetState,
        handleSelectCommand,
        executeCommand,
        executeChain,
        startListening,
        stopListening
    } = actions;

    const handleInternalClose = () => {
        resetState();
        onClose();
    };

    if (commandResult) {
        return <CommandResultView result={commandResult} onDone={handleInternalClose} />;
    }

    if (commandForParams) {
        return (
            <ParameterWeaver
                key={commandForParams.commandId}
                command={commandForParams}
                onSubmit={(p) => void executeCommand(commandForParams, p)}
                onCancel={() => {
                    actions.setCommandForParams(null);
                }}
            />
        );
    }

    const inputPlaceholder = isClcMode
        ? 'Add command to chain...'
        : isListening
          ? 'Listening...'
          : 'Transmit directive...';

    return (
        <div className="flex h-[600px]">
            <div className={`flex-1 flex flex-col border-r border-${String(theme.primary)}-500/20`}>
                <div className={`p-4 border-b border-${String(theme.primary)}-500/20 flex items-center gap-3`}>
                    {isFiring ? (
                        <Loader className="w-5 h-5 animate-spin" />
                    ) : (
                        <Search className={`w-5 h-5 text-${String(theme.primary)}-400`} />
                    )}
                    <input
                        ref={inputRef}
                        type="text"
                        value={searchQuery}
                        onChange={(e) => {
                            setSearchQuery(e.target.value);
                        }}
                        onKeyDown={(e) => {
                            if (e.key === 'ArrowDown')
                                setSelectedIndex(Math.min(selectedIndex + 1, filteredCommands.length - 1));
                            if (e.key === 'ArrowUp') setSelectedIndex(Math.max(selectedIndex - 1, 0));
                            if (e.key === 'Enter') handleSelectCommand(filteredCommands[selectedIndex]);
                            if (e.key === 'Escape') handleInternalClose();
                        }}
                        placeholder={inputPlaceholder}
                        className="flex-1 bg-transparent border-none outline-none text-cyan-100 placeholder-cyan-500/30"
                        autoFocus
                    />
                    <div className="flex items-center gap-2">
                        {isClcMode && (
                            <Tooltip label="Execute Chain">
                                <button
                                    onClick={() => {
                                        void executeChain();
                                    }}
                                    disabled={currentConstruction.length === 0}
                                    className={`p-1.5 rounded-md bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/40 transition-all ${
                                        currentConstruction.length === 0 ? 'opacity-20' : 'animate-pulse'
                                    }`}
                                >
                                    <Play size={16} />
                                </button>
                            </Tooltip>
                        )}
                        {isGlobal && (
                            <button
                                onClick={isListening ? stopListening : startListening}
                                className={`p-1.5 rounded-full ${
                                    isListening ? 'bg-red-500/20 text-red-400 animate-pulse' : 'text-cyan-400/50'
                                }`}
                            >
                                {isListening ? <Mic size={16} /> : <MicOff size={16} />}
                            </button>
                        )}
                    </div>
                </div>

                {isClcMode && (
                    <div className={`px-4 py-3 bg-cyan-900/10 border-b border-cyan-500/20 flex flex-col gap-2`}>
                        <div className="flex items-center justify-between">
                            <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-cyan-400/60">
                                Construction Chain
                            </span>
                            <button
                                onClick={() => {
                                    actions.setCurrentConstruction([]);
                                }}
                                className="text-cyan-500/40 hover:text-red-400 transition-colors"
                            >
                                <Trash2 size={12} />
                            </button>
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {currentConstruction.map((cmd, i) => (
                                <div
                                    key={i}
                                    className="flex items-center gap-2 px-2 py-1 bg-cyan-500/10 border border-cyan-500/20 rounded text-[10px] font-mono text-cyan-200"
                                >
                                    {cmd.commandId}
                                    {i < currentConstruction.length - 1 && (
                                        <ArrowRight size={10} className="text-cyan-500/40" />
                                    )}
                                </div>
                            ))}
                            {currentConstruction.length === 0 && (
                                <span className="text-[10px] text-cyan-500/20 italic">
                                    Empty chain. Select commands below.
                                </span>
                            )}
                        </div>
                    </div>
                )}

                {visualContext && (
                    <div className="px-4 py-2 bg-indigo-500/10 border-b border-indigo-500/20 flex items-center justify-between text-[10px] text-indigo-300">
                        <div className="flex items-center gap-2">
                            <ImageIcon size={12} />
                            <span>Multi-Modal Context: {visualContext.name}</span>
                        </div>
                        <button
                            onClick={() => {
                                setVisualContext(null);
                            }}
                            className="hover:text-red-400"
                        >
                            Remove
                        </button>
                    </div>
                )}

                <div className="flex-1 overflow-y-auto scrollbar-thin p-2">
                    {filteredCommands.map((cmd, index) => (
                        <button
                            key={cmd.commandId}
                            onClick={() => {
                                handleSelectCommand(cmd);
                            }}
                            className={`w-full text-left px-3 py-3 rounded-lg flex items-center justify-between group transition-all duration-200 ${
                                index === selectedIndex
                                    ? `bg-${String(theme.primary)}-500/20 text-white`
                                    : 'text-cyan-400/70 hover:bg-white/5'
                            }`}
                        >
                            <div className="flex flex-col">
                                <span className="font-mono text-sm">{cmd.commandId}</span>
                                <span className="text-[10px] opacity-40 group-hover:opacity-60 truncate max-w-[400px]">
                                    {cmd.description}
                                </span>
                            </div>
                            <div className="flex items-center gap-2">
                                {isClcMode && cmd.commandId !== 'CMD_BEGIN_CLC' && (
                                    <ListPlus size={14} className="text-cyan-400/30 group-hover:text-cyan-400" />
                                )}
                                {cmd.isEcho && <Lightbulb size={14} className="text-amber-400 animate-pulse" />}
                            </div>
                        </button>
                    ))}
                </div>
            </div>
            <div className={`w-[360px] bg-black/20 flex flex-col border-l border-${String(theme.primary)}-500/20`}>
                <CommandPreview command={filteredCommands[selectedIndex] || null} />
            </div>
        </div>
    );
};

interface TheSynapseProps {
    isOpen: boolean;
    onClose: () => void;
}

const TheSynapse: React.FC<TheSynapseProps> = ({ isOpen, onClose }) => {
    const theme = useTheme();
    const addNovaSpark = useCoherenceStore((state) => state.addNovaSpark);

    const handlePaste = (e: React.ClipboardEvent) => {
        // This is handled by a listener in useSynapseLogic usually, 
        // but since we want to keep paste logic global, we can wrap it here or pass a ref.
        // For simplicity, we'll let SynapseInterface handle internal context if needed.
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4" onPaste={handlePaste}>
            <div className="fixed inset-0 bg-black/80 backdrop-blur-sm" onClick={onClose} />
            <div
                className={`relative w-full max-w-4xl min-h-[500px] bg-gray-900 border border-${String(
                    theme.primary,
                )}-500/30 rounded-xl shadow-2xl flex flex-col overflow-hidden animate-scale-in transition-all duration-300`}
            >
                <SynapseInterface 
                    onClose={onClose} 
                    onNovaSpark={addNovaSpark} 
                    isGlobal={true}
                />
                <div
                    className={`h-1 bg-gradient-to-r from-${String(theme.primary)}-900 via-${String(
                        theme.primary,
                    )}-500 to-${String(theme.primary)}-900 opacity-50`}
                />
            </div>
        </div>
    );
};

export default TheSynapse;


