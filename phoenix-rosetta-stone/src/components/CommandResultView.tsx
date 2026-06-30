import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    CheckCircle,
    AlertTriangle,
    ListChecks,
    CornerDownLeft,
    Database,
    Unplug,
    Loader,
    Layout,
    ShieldCheck,
    Zap,
    ChevronRight,
    BrainCircuit,
    Code,
} from 'lucide-react';
import { DispatchResult } from '@essence/types';
import { dispatchCommand, connectLocalFsCommand } from '../services';

interface CommandResultViewProps {
    result: DispatchResult;
    onDone: () => void;
}

const CommandResultView: React.FC<CommandResultViewProps> = ({ result, onDone }) => {
    const navigate = useNavigate();
    const [isRecovering, setIsRecovering] = useState(false);

    const handleGoToLoom = () => {
        onDone();
        void navigate('/loom');
    };

    const handleEstablishLink = async () => {
        setIsRecovering(true);
        const connectionResult = await dispatchCommand(connectLocalFsCommand, {});
        setIsRecovering(false);
        if (connectionResult.success) {
            onDone(); // Close synapse on successful connection
        }
    };

    interface ScanResult {
        dissonancesFound?: number;
        stats?: Record<string, unknown>;
    }
    interface Artifact {
        id: string;
        name: string;
        description: string;
        type: string;
    }
    interface ArtifactMetadata {
        id: string;
        title: string;
        type: string;
        contentSnippet: string;
    }
    interface ArtifactList {
        artifacts: Artifact[];
    }
    interface RepairResult {
        repairedVectors: string[];
        integrityScore: number;
        anomaliesResolved: number;
        bonus: string;
    }
    interface ChainResult {
        log: string[];
    }
    interface PatchResult {
        patchedFile: string;
    }

    const isScanResult = result.data?.dissonancesFound !== undefined;
    const isArtifactMetadata = Boolean(result.data?.id && result.data.type);
    const isArtifactList = Boolean(result.data && Array.isArray(result.data.artifacts));
    const isRepairResult = Boolean(result.data?.repairedVectors);
    const isChainResult = Boolean(result.data && Array.isArray(result.data.log));
    const isPatchResult = Boolean(result.data?.patchedFile);
    const isNeuralError = Boolean(result.data?.isNeuralError);

    const scanData = result.data as unknown as ScanResult | undefined;
    const metadata = result.data as unknown as ArtifactMetadata | undefined;
    const artifactListData = result.data as unknown as ArtifactList | undefined;
    const repairData = result.data as unknown as RepairResult | undefined;
    const chainData = result.data as unknown as ChainResult | undefined;
    const patchData = result.data as unknown as PatchResult | undefined;

    return (
        <div className="p-6 h-full flex flex-col items-center justify-center text-center animate-fade-in-sm">
            {result.success ? (
                <CheckCircle
                    className={`w-16 h-16 ${isRepairResult ? 'text-amber-400' : 'text-green-400'} drop-shadow-[0_0_8px_currentColor] mb-4`}
                />
            ) : (
                <AlertTriangle
                    className={`w-16 h-16 ${isNeuralError ? 'text-amber-400' : 'text-red-400'} drop-shadow-[0_0_8px_currentColor] mb-4`}
                />
            )}

            <h3 className="text-2xl font-light text-cyan-100">
                {result.success
                    ? isRepairResult
                        ? 'Maintenance Complete'
                        : isChainResult
                          ? 'Chain Execution Complete'
                          : isPatchResult
                            ? 'Code Repair Successful'
                            : 'Execution Successful'
                    : 'Execution Dissonance'}
            </h3>
            <p className="text-cyan-300/90 mt-2 max-w-md">{result.message}</p>

            {/* Actionable Recovery Path for Neural Link */}
            {!result.success && isNeuralError && (
                <div className="mt-8 flex flex-col items-center gap-4 animate-fade-in-up">
                    <button
                        onClick={() => {
                            void handleEstablishLink();
                        }}
                        disabled={isRecovering}
                        className="flex items-center gap-3 px-6 py-3 bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-400/50 rounded-lg text-cyan-100 font-medium transition-all shadow-[0_0_15px_rgba(34,211,238,0.2)]"
                    >
                        {isRecovering ? <Loader className="animate-spin" size={18} /> : <Unplug size={18} />}
                        Establish Neural Link
                    </button>
                    <p className="text-[10px] text-cyan-500/60 uppercase tracking-widest font-mono">
                        Mandatory Handshake Required
                    </p>
                </div>
            )}

            {/* Code Patch Success View */}
            {result.success && isPatchResult && patchData && (
                <div className="mt-6 w-full max-w-lg bg-black/40 rounded-lg border border-emerald-500/30 overflow-hidden text-left shadow-2xl animate-fade-in-up">
                    <div className="bg-emerald-900/20 p-3 border-b border-emerald-500/20 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Code size={14} className="text-emerald-400" />
                            <span className="text-xs font-mono text-emerald-200 uppercase tracking-widest">
                                Patch Applied
                            </span>
                        </div>
                        <span className="text-[10px] font-mono text-emerald-500/60">Verified Artifact</span>
                    </div>
                    <div className="p-4">
                        <p className="text-xs text-gray-500 uppercase mb-1">Target Sector</p>
                        <p className="text-sm text-emerald-300 font-mono truncate">{patchData.patchedFile}</p>
                        <div className="mt-4 pt-4 border-t border-white/5 flex items-center gap-2 text-[10px] text-emerald-400/70 italic">
                            <ShieldCheck size={12} /> Architectural integrity has been manually restored.
                        </div>
                    </div>
                </div>
            )}

            {/* CLC Chain Log View */}
            {isChainResult && chainData && (
                <div className="mt-6 w-full max-w-xl bg-black/40 rounded-lg border border-cyan-500/30 overflow-hidden text-left shadow-2xl animate-fade-in-up">
                    <div className="bg-cyan-900/20 p-3 border-b border-cyan-500/20 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <BrainCircuit size={14} className="text-cyan-400" />
                            <span className="text-xs font-mono text-cyan-200 uppercase tracking-widest">
                                Neural Chain Log
                            </span>
                        </div>
                        <span className="text-[10px] font-mono text-cyan-500/60">
                            Neurons Fired: {chainData.log.length}
                        </span>
                    </div>
                    <div className="max-h-[250px] overflow-y-auto scrollbar-thin p-3 space-y-2">
                        {chainData.log.map((line, i) => (
                            <div
                                key={i}
                                className="flex gap-2 text-xs font-mono p-2 bg-white/5 rounded border border-white/5"
                            >
                                <ChevronRight size={14} className="text-cyan-500 shrink-0 mt-0.5" />
                                <span className="text-cyan-200/80">{line}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Specialized Repair Result View */}
            {result.success && isRepairResult && repairData && (
                <div className="mt-6 w-full max-w-lg bg-black/40 rounded-lg border border-amber-500/30 overflow-hidden text-left shadow-2xl animate-fade-in-up">
                    <div className="bg-amber-900/20 p-3 border-b border-amber-500/20 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <ShieldCheck size={14} className="text-amber-400" />
                            <span className="text-xs font-mono text-amber-200 uppercase tracking-widest">
                                Integrity Restoration Report
                            </span>
                        </div>
                        <div className="flex items-center gap-1.5">
                            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                            <span className="text-[10px] font-mono text-emerald-400">OPTIMAL</span>
                        </div>
                    </div>
                    <div className="p-4 space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-3 bg-white/5 rounded border border-white/5">
                                <p className="text-[9px] text-gray-500 uppercase mb-1">Integrity Score</p>
                                <p className="text-xl font-mono text-amber-300">
                                    {(repairData.integrityScore * 100).toFixed(0)}%
                                </p>
                            </div>
                            <div className="p-3 bg-white/5 rounded border border-white/5">
                                <p className="text-[9px] text-gray-500 uppercase mb-1">Anomalies Resolved</p>
                                <p className="text-xl font-mono text-amber-300">{repairData.anomaliesResolved}</p>
                            </div>
                        </div>
                        <div>
                            <p className="text-[10px] text-gray-500 uppercase mb-2">Restored Vectors</p>
                            <div className="flex flex-wrap gap-2">
                                {repairData.repairedVectors.map((v) => (
                                    <span
                                        key={v}
                                        className="px-2 py-0.5 bg-amber-500/10 border border-amber-500/20 rounded-full text-[10px] font-mono text-amber-200"
                                    >
                                        {v}
                                    </span>
                                ))}
                            </div>
                        </div>
                        <div className="pt-2 flex items-center gap-2 text-[10px] text-cyan-400/70 italic border-t border-white/5">
                            <Zap size={10} className="text-amber-400" />
                            {repairData.bonus}
                        </div>
                    </div>
                </div>
            )}

            {result.success && isScanResult && (scanData?.dissonancesFound ?? 0) > 0 && (
                <button
                    onClick={handleGoToLoom}
                    className="mt-6 flex items-center gap-2 px-4 py-2 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-400/30 rounded-md text-cyan-200 transition-all"
                >
                    <ListChecks size={16} /> View Tasks in The Loom
                </button>
            )}

            {isArtifactList && artifactListData && (
                <div className="mt-6 w-full max-w-xl bg-black/40 rounded-lg border border-cyan-500/30 overflow-hidden text-left shadow-lg">
                    <div className="bg-cyan-900/20 p-3 border-b border-cyan-500/10 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Layout size={14} className="text-cyan-400" />
                            <span className="text-xs font-mono text-cyan-200 uppercase tracking-widest">
                                Protocol Registry catalog
                            </span>
                        </div>
                        <span className="text-[10px] font-mono text-cyan-500/60">
                            Count: {artifactListData.artifacts.length}
                        </span>
                    </div>
                    <div className="max-h-[300px] overflow-y-auto scrollbar-thin p-2 space-y-1">
                        {artifactListData.artifacts.map((art) => (
                            <div
                                key={art.id}
                                className="p-2 hover:bg-white/5 rounded transition-colors flex items-center justify-between gap-4 border border-transparent hover:border-white/10"
                            >
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm text-cyan-100 truncate">{art.name}</p>
                                    <p className="text-[10px] text-cyan-400/40 truncate">{art.description}</p>
                                </div>
                                <span className="text-[9px] font-mono bg-cyan-500/10 px-1.5 py-0.5 rounded text-cyan-400 shrink-0">
                                    {art.type}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {isArtifactMetadata && metadata && (
                <div className="mt-6 w-full max-w-lg bg-black/40 rounded-lg border border-indigo-500/30 overflow-hidden text-left shadow-lg">
                    <div className="bg-indigo-900/20 p-3 border-b border-indigo-500/20 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Database size={14} className="text-indigo-400" />
                            <span className="text-xs font-mono text-indigo-200 uppercase tracking-widest">
                                Artifact Metadata
                            </span>
                        </div>
                        <span className="text-[10px] font-mono text-indigo-400/60">ID: {metadata.id}</span>
                    </div>
                    <div className="p-4 space-y-3">
                        <div>
                            <span className="text-[10px] text-gray-500 uppercase block mb-1">Title</span>
                            <span className="text-sm text-cyan-100">{metadata.title}</span>
                        </div>
                        <div>
                            <span className="text-[10px] text-gray-500 uppercase block mb-1">Type</span>
                            <span className="text-xs font-mono text-indigo-300 bg-indigo-500/10 px-1.5 py-0.5 rounded">
                                {metadata.type}
                            </span>
                        </div>
                        <div>
                            <span className="text-[10px] text-gray-500 uppercase block mb-1">Content Snippet</span>
                            <p className="text-xs text-cyan-200/70 italic leading-relaxed">
                                {metadata.contentSnippet}...
                            </p>
                        </div>
                    </div>
                </div>
            )}

            <button
                onClick={onDone}
                className="mt-8 flex items-center gap-2 px-4 py-2 bg-gray-700/30 hover:bg-gray-700/60 border border-gray-600/50 rounded-md text-cyan-300 transition-colors"
            >
                Done <CornerDownLeft size={16} />
            </button>

            <style>{`
        @keyframes fade-in-up {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-up { animation: fade-in-up 0.6s ease-out forwards; }
        .scrollbar-thin::-webkit-scrollbar { width: 4px; }
        .scrollbar-thin::-webkit-scrollbar-thumb { background-color: rgba(34, 211, 238, 0.2); border-radius: 20px; }
      `}</style>
        </div>
    );
};

export default CommandResultView;
