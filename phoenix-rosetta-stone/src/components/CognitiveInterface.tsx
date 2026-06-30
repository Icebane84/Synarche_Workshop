import { Database, Globe, Sparkles } from 'lucide-react';
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useTheme } from '../hooks/useTheme';
import { commandRegistry, dispatchCommand, interpretNaturalLanguageCommand, queryCognitiveCore, searchWithCognitiveCore } from '../services';
import { useCoherenceStore } from '../store/coherenceStore';
import { useTaskStore } from '../store/taskStore';
import { GroundedResponse, SystemContext } from '@essence/types';
import Tooltip from './common/Tooltip';

const Spinner: React.FC<{ color: string }> = ({ color }) => (
    <svg
        className={`animate-spin h-5 w-5 text-${color}-300`}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
    >
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
        <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
    </svg>
);

const CognitiveInterface: React.FC = () => {
    const [prompt, setPrompt] = useState<string>('');
    const [response, setResponse] = useState<GroundedResponse | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [useSearch, setUseSearch] = useState<boolean>(false);
    const [activeToolCall, setActiveToolCall] = useState<string | null>(null);

    const pulse = useCoherenceStore((state) => state.pulse);
    const addNovaSpark = useCoherenceStore((state) => state.addNovaSpark);
    const location = useLocation();
    const theme = useTheme();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!prompt.trim() || isLoading) return;

        setIsLoading(true);
        setError(null);
        setResponse(null);
        setActiveToolCall(null);

        // Dynamic Context Injection
        // We snapshot the current state of the application to give the AI awareness of the "Now".
        const systemContext: SystemContext = {
            tasks: useTaskStore.getState().tasks,
            coherence: {
                index: useCoherenceStore.getState().coherenceIndex,
                focus: useCoherenceStore.getState().cognitiveFocus,
                stats: useCoherenceStore.getState().coreStats,
            },
            currentLocation: location.pathname,
        };

        try {
            if (useSearch) {
                const result = await searchWithCognitiveCore(prompt, systemContext);
                setResponse(result);
                pulse();
                setIsLoading(false);
                return;
            }

            // 1. Check for LOCAL COMMAND ALIAS matches first to bypass AI failures
            const interpretedId = await interpretNaturalLanguageCommand(prompt);
            const localCommand = interpretedId ? commandRegistry[interpretedId] : null;

            if (localCommand?.parameters.length === 0) {
                setActiveToolCall(`Direct Interface: Executing ${localCommand.commandId}...`);
                const result = await dispatchCommand(localCommand, { visualContext: null });

                if (result.success) {
                    addNovaSpark(`Neural Interface: Local bypass activated for ${localCommand.commandId}.`);
                    setResponse({
                        text: `[System Sync] Direct Command Executed: ${localCommand.commandId}\n\n${result.message}`,
                        sources: [],
                    });
                } else {
                    setError(`Local Execution Failed: ${result.message}`);
                }
                setIsLoading(false);
                pulse();
                return;
            }

            // 2. Fallback to Gemini LLM for interpretation or general chat
            const { text, toolCall } = await queryCognitiveCore(prompt, systemContext);
            setResponse({ text, sources: [] });

            if (toolCall) {
                setActiveToolCall(`Executing ${toolCall.name}...`);

                const command = commandRegistry[toolCall.name];
                if (command) {
                    try {
                        const result = await dispatchCommand(command, toolCall.args);

                        if (result.success) {
                            addNovaSpark(`Neural Forge: Executed ${toolCall.name}.`);
                            setActiveToolCall(`Execution Complete: ${toolCall.name}`);

                            // Append tool output to chat for visibility
                            const outputText = result.data
                                ? `\n\n[Tool Output]\n${JSON.stringify(result.data, null, 2)}`
                                : `\n\n[System Notification] ${result.message}`;

                            setResponse((prev) => {
                                if (!prev) return prev;
                                return {
                                    ...prev,
                                    text: (prev.text || '') + outputText,
                                };
                            });
                        } else {
                            setError(`Execution Failed: ${result.message}`);
                            setActiveToolCall(null);
                        }
                    } catch (err) {
                        const msg = err instanceof Error ? err.message : 'Unknown dispatch error';
                        setError(`Dispatch Error: ${msg}`);
                        setActiveToolCall(null);
                    }
                } else {
                    setError(`Unknown Protocol: ${toolCall.name} is not in the registry.`);
                    setActiveToolCall(null);
                }
            }

            pulse(); // Trigger a pulse in the "Shared Consciousness"
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred.';
            setError(`Failed to query cognitive core: ${errorMessage}`);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
        void handleSubmit(e);
    };

    return (
        <div
            className={`w-full max-w-4xl p-4 border border-${theme.primary}-500/20 bg-black/30 backdrop-blur-md rounded-lg transition-colors duration-500`}
        >
            <form onSubmit={handleFormSubmit}>
                <div className="flex items-center gap-3">
                    <textarea
                        value={prompt}
                        onChange={(e) => {
                            setPrompt(e.target.value);
                        }}
                        placeholder="Transmit a thought to the Cognitive Core..."
                        rows={2}
                        className={`flex-1 bg-${theme.primary}-900/10 border border-${theme.primary}-400/30 rounded-md p-3 text-${theme.primary}-200 placeholder-${theme.primary}-400/50 focus:outline-none focus:ring-2 focus:ring-${theme.primary}-300/80 focus:shadow-[0_0_15px_rgba(100,220,255,0.5)] transition-all duration-300 resize-none`}
                        disabled={isLoading}
                    />
                    <Tooltip label="Transmit thought to the Cognitive Core">
                        <button
                            type="submit"
                            disabled={isLoading || !prompt.trim()}
                            className={`flex items-center justify-center gap-2 px-4 py-2 bg-${theme.primary}-500/20 hover:bg-${theme.primary}-500/40 border border-${theme.primary}-400/50 rounded-md text-${theme.primary}-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 hover:drop-shadow-[0_0_8px_rgba(100,220,255,0.7)] disabled:hover:drop-shadow-none`}
                        >
                            {isLoading ? <Spinner color={theme.primary} /> : 'Transmit'}
                        </button>
                    </Tooltip>
                </div>
                <div className="flex justify-between mt-2 items-center">
                    {isLoading && !useSearch && (
                        <div className="flex items-center gap-2 text-xs text-amber-300/80 animate-pulse">
                            <Database size={12} /> Accessing Neural Archives (RAG)...
                        </div>
                    )}
                    {!isLoading && <div className="flex-1" />}

                    <Tooltip label="Ground response in real-time web data using Google Search.">
                        <label
                            className={`flex items-center gap-2 cursor-pointer text-xs text-${theme.primary}-400/70 hover:text-${theme.primary}-200 transition-colors`}
                        >
                            <input
                                type="checkbox"
                                checked={useSearch}
                                onChange={(e) => {
                                    setUseSearch(e.target.checked);
                                }}
                                className={`w-4 h-4 bg-${theme.primary}-900/20 border-${theme.primary}-500/50 text-${theme.primary}-400 focus:ring-${theme.primary}-500/50 rounded`}
                            />
                            Ground with Google Search
                        </label>
                    </Tooltip>
                </div>
            </form>

            {activeToolCall && (
                <div className="mt-4 p-3 bg-indigo-900/20 border border-indigo-500/30 rounded-md flex items-center gap-3 animate-pulse">
                    <Sparkles size={16} className="text-indigo-400" />
                    <span className="text-sm text-indigo-200 font-mono tracking-wide">{activeToolCall}</span>
                </div>
            )}

            {response && (
                <div
                    className={`mt-4 p-4 bg-black/20 border border-${theme.primary}-500/10 rounded-md animate-fade-in-sm`}
                >
                    <h3 className={`text-sm font-light tracking-widest text-${theme.primary}-400/70 mb-2`}>
                        RESPONSE:
                    </h3>
                    <p className={`text-${theme.primary}-300 whitespace-pre-wrap`}>{response.text}</p>

                    {response.sources.length > 0 && (
                        <div className={`mt-4 pt-3 border-t border-${theme.primary}-500/10`}>
                            <h4
                                className={`text-xs font-light tracking-widest text-${theme.primary}-400/60 mb-2 flex items-center gap-2`}
                            >
                                <Globe size={14} /> GROUNDED ON:
                            </h4>
                            <ul className="space-y-1">
                                {response.sources.map((source, index) => (
                                    <li key={index}>
                                        <a
                                            href={source.uri}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className={`text-xs text-${theme.primary}-400 hover:text-${theme.primary}-200 hover:underline transition-colors truncate block`}
                                            title={source.uri}
                                        >
                                            {`[${(index + 1).toString()}] ${source.title}`}
                                        </a>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}

            {error && (
                <div className="mt-4 p-4 bg-red-900/30 border border-red-500/30 rounded-md">
                    <h3 className="text-sm font-light tracking-widest text-red-300/70 mb-2">ERROR:</h3>
                    <p className="text-red-200">{error}</p>
                </div>
            )}
            <style>{`
        @keyframes fade-in-sm {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .animate-fade-in-sm { animation: fade-in-sm 0.5s ease-out forwards; }
      `}</style>
        </div>
    );
};

export default CognitiveInterface;
