// [OMEGA AST Cleaned]: Tokenized design standards applied.
import {
    Activity,
    AlertTriangle,
    ArrowRight,
    CheckCircle,
    Copy,
    Database,
    Loader,
    Shield,
    Terminal,
    Unplug,
} from 'lucide-react';
import React, { useEffect, useRef } from 'react';
import { useProtocolIgnition } from '../../../hooks/useProtocolIgnition';
import { useFileSystemStore } from '../../../store/fileSystemStore';
import { useTaskStore } from '../../../store/taskStore';
import Tooltip from '../../common/Tooltip';

/**
 * @fileoverview Component for the Phoenix Protocol Ignition sequence.
 * Managed by useProtocolIgnition hook.
 */
export const ProtocolIgnition: React.FC = () => {
    const isConnected = useFileSystemStore((state) => state.isConnected);
    const isSimulationMode = useTaskStore((state) => state.isSimulationMode);

    const {
        step,
        isProcessing,
        results,
        ignitionLogs,
        showFixCommand,
        runAudit,
        runSync,
        establishLink,
        copyFixCommand,
    } = useProtocolIgnition();

    const logEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [ignitionLogs]);

    if (isConnected || isSimulationMode) return null;

    return (
        <div className="w-full max-w-4xl p-6 bg-amber-500/5 border border-amber-500/20 rounded-xl backdrop-blur-md animate-fade-in-up shadow-[0_0_40px_rgba(245,158,11,0.05)]">
            <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-amber-500/20 rounded-lg animate-pulse">
                        <AlertTriangle className="text-amber-400" size={24} />
                    </div>
                    <div>
                        <h3 className="text-xl font-light text-amber-200 tracking-wider">System Readiness Required</h3>
                        <p className="text-xs text-amber-400/60 uppercase tracking-widest font-mono">
                            Phoenix Protocol Ignition Sequence
                        </p>
                    </div>
                </div>
                <div className="flex gap-1">
                    {[1, 2, 3].map((i) => (
                        <div
                            key={i}
                            className={`w-8 h-1 rounded-full transition-all duration-500 ${
                                step >= i ? 'bg-amber-400' : 'bg-white/10'
                            }`}
                        />
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {/* Step 1: Substrate Audit */}
                <div
                    className={`relative p-5 rounded-lg border transition-all duration-500 ${
                        step === 1
                            ? 'bg-amber-500/10 border-amber-400/50 shadow-[0_0_20px_rgba(245,158,11,0.1)]'
                            : 'bg-black/20 border-white/5 opacity-50'
                    }`}
                >
                    <div className="flex items-center justify-between mb-3">
                        <div
                            className={`p-2 rounded-md ${
                                results[1]?.success ? 'bg-emerald-500/20' : 'bg-amber-500/10'
                            }`}
                        >
                            <Shield size={20} className={results[1]?.success ? 'text-emerald-400' : 'text-amber-400'} />
                        </div>
                        {results[1]?.success && <CheckCircle size={16} className="text-emerald-400 animate-fade-in" />}
                    </div>
                    <h4 className="text-sm font-semibold text-cyan-100 tracking-tight">Audit Substrate</h4>
                    <p className="text-[10px] text-cyan-400/60 mt-1.5 leading-relaxed">
                        Analyze sectors for structural dissonance and script permissions.
                    </p>

                    <div className="mt-6">
                        {step === 1 && !results[1]?.success && (
                            <button
                                onClick={() => void runAudit()}
                                disabled={isProcessing}
                                className="group w-full py-2 bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 text-[10px] uppercase font-bold rounded border border-amber-500/30 transition-all flex items-center justify-center gap-2"
                            >
                                {isProcessing ? (
                                    <Loader size={12} className="animate-spin" />
                                ) : (
                                    <>
                                        Initiate Audit{' '}
                                        <ArrowRight
                                            size={10}
                                            className="group-hover:translate-x-1 transition-transform"
                                        />
                                    </>
                                )}
                            </button>
                        )}
                        {results[1]?.success && (
                            <div className="text-[10px] font-mono text-emerald-400/80 bg-emerald-500/5 p-2 rounded border border-emerald-500/10">
                                Dissonances:{' '}
                                {(results[1]?.data as { dissonancesFound?: number } | undefined)?.dissonancesFound ??
                                    'Unknown'}
                            </div>
                        )}
                        {!results[1]?.success && !isProcessing && showFixCommand && (
                            <button
                                onClick={copyFixCommand}
                                className="mt-2 w-full py-1.5 bg-gray-800 hover:bg-gray-700 text-cyan-300 text-[8px] uppercase font-bold rounded flex items-center justify-center gap-2 border border-cyan-500/20"
                            >
                                <Copy size={10} /> Copy Windows Fix
                            </button>
                        )}
                    </div>
                </div>

                {/* Step 2: Metadata Sync */}
                <div
                    className={`relative p-5 rounded-lg border transition-all duration-500 ${
                        step === 2
                            ? 'bg-amber-500/10 border-amber-400/50 shadow-[0_0_20px_rgba(245,158,11,0.1)]'
                            : 'bg-black/20 border-white/5 opacity-50'
                    }`}
                >
                    <div className="flex items-center justify-between mb-3">
                        <div
                            className={`p-2 rounded-md ${
                                results[2]?.success ? 'bg-emerald-500/20' : 'bg-amber-500/10'
                            }`}
                        >
                            <Database
                                size={20}
                                className={results[2]?.success ? 'text-emerald-400' : 'text-amber-400'}
                            />
                        </div>
                        {results[2]?.success && <CheckCircle size={16} className="text-emerald-400 animate-fade-in" />}
                    </div>
                    <h4 className="text-sm font-semibold text-cyan-100 tracking-tight">Sync Metadata</h4>
                    <p className="text-[10px] text-cyan-400/60 mt-1.5 leading-relaxed">
                        Hydrate neural pathways with core definitions via Cloud Relay.
                    </p>

                    <div className="mt-6">
                        {step === 2 && !results[2]?.success && (
                            <button
                                onClick={() => void runSync()}
                                disabled={isProcessing}
                                className="group w-full py-2 bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 text-[10px] uppercase font-bold rounded border border-amber-500/30 transition-all flex items-center justify-center gap-2"
                            >
                                {isProcessing ? (
                                    <Loader size={12} className="animate-spin" />
                                ) : (
                                    <>
                                        Sync Path{' '}
                                        <ArrowRight
                                            size={10}
                                            className="group-hover:translate-x-1 transition-transform"
                                        />
                                    </>
                                )}
                            </button>
                        )}
                        {results[2]?.success && (
                            <div className="text-[10px] font-mono text-emerald-400/80 bg-emerald-500/5 p-2 rounded border border-emerald-500/10">
                                Vector Space: HYDRATED
                            </div>
                        )}
                    </div>
                </div>

                {/* Step 3: Neural Link */}
                <div
                    className={`relative p-5 rounded-lg border transition-all duration-500 ${
                        step === 3
                            ? 'bg-cyan-500/10 border-cyan-400/50 shadow-[0_0_20px_rgba(34,211,238,0.1)]'
                            : 'bg-black/20 border-white/5 opacity-50'
                    }`}
                >
                    <div className="flex items-center justify-between mb-3">
                        <div className="p-2 bg-cyan-500/10 rounded-md">
                            <Unplug size={20} className="text-cyan-400" />
                        </div>
                        {step === 3 && <Activity size={16} className="text-cyan-400 animate-pulse" />}
                    </div>
                    <h4 className="text-sm font-semibold text-cyan-100 tracking-tight">Neural Link</h4>
                    <p className="text-[10px] text-cyan-400/60 mt-1.5 leading-relaxed">
                        Enable deeper deeper deeper analysis via physical codebase bridge.
                    </p>

                    <div className="mt-6">
                        {step === 3 && (
                            <button
                                onClick={() => void establishLink()}
                                disabled={isProcessing}
                                className="group w-full py-2 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-200 text-[10px] uppercase font-bold rounded border border-cyan-400/50 transition-all shadow-[0_0_15px_rgba(34,211,238,0.2)] flex items-center justify-center gap-2"
                            >
                                {isProcessing ? (
                                    <Loader size={12} className="animate-spin" />
                                ) : (
                                    <>
                                        Bridge Synapse <Activity size={12} className="group-hover:animate-bounce" />
                                    </>
                                )}
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Terminal Log Output */}
            <div className="bg-black/40 border border-white/10 rounded-lg p-3 font-mono text-[10px] text-emerald-400/80 mb-4 h-32 flex flex-col">
                <div className="flex items-center gap-2 border-b border-white/5 pb-1 mb-1 text-gray-500 uppercase tracking-widest font-bold">
                    <Terminal size={10} /> Substrate Ignition Logs
                </div>
                <div className="flex-1 overflow-y-auto scrollbar-none">
                    {ignitionLogs.map((log, i) => (
                        <div key={`${i}-${log.substring(0, 10)}`} className="mb-0.5">
                            <span className="text-emerald-500/40 mr-2">»</span>
                            {log}
                        </div>
                    ))}
                    <div ref={logEndRef} />
                </div>
            </div>

            <div className="mt-4 pt-4 border-t border-white/5 flex items-center justify-between text-[9px] font-mono text-amber-500/40 uppercase tracking-tighter">
                <div className="flex items-center gap-4">
                    <span>Protocol: Ignition-v4.2</span>
                    <span className="flex items-center gap-2">
                        <div className="w-1 h-1 rounded-full bg-amber-500/40 animate-ping" />
                        Awaiting Handshake
                    </span>
                </div>
                <Tooltip label="Physical Handshake for Windows Architects">
                    <span className="text-gray-500 italic">Prerequisite: Set-ExecutionPolicy RemoteSigned</span>
                </Tooltip>
            </div>
        </div>
    );
};
