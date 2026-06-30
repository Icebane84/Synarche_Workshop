import { Activity, Brain, Database, ShieldCheck } from 'lucide-react';
import React from 'react';
import { useParams } from 'react-router-dom';
import { MetaEngine, SystemBiometrics } from '../../components';
import { useTheme } from '../../hooks/useTheme';
import { commandRegistry } from '../../services';
import { useCoherenceStore } from '../../store/coherenceStore';
import { useLogStore } from '../../store/logStore';

const MemoryCoreView: React.FC = () => {
    const logs = useLogStore((state) => state.logs);
    const theme = useTheme();

    return (
        <div className="space-y-6 animate-fade-in">
            <MetaEngine />
            <div className="grid grid-cols-1 gap-4">
                <h3 className={`text-xl font-light text-${theme.primary}-200 flex items-center gap-2 mb-4`}>
                    <Database size={20} /> Archival Experience Stream
                </h3>
                <div className="space-y-4">
                    {logs.length > 0 ? (
                        logs.map((log) => (
                            <div
                                key={log.logId}
                                className="p-4 bg-black/40 border border-white/5 rounded-lg hover:border-cyan-500/30 transition-all group"
                            >
                                <div className="flex justify-between items-center mb-2">
                                    <span className="text-[10px] font-mono text-cyan-500/60">{log.logId}</span>
                                    <span className="text-[10px] font-mono text-gray-500">
                                        {new Date(log.timestamp).toLocaleTimeString()}
                                    </span>
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <p className="text-[9px] uppercase text-gray-500 mb-1">User Intent</p>
                                        <p className="text-sm text-cyan-100">{log.userTurn.analysis.inferredIntent}</p>
                                    </div>
                                    <div>
                                        <p className="text-[9px] uppercase text-gray-500 mb-1">Consistency</p>
                                        <p
                                            className={`text-sm ${log.phenomenologicalState.internalConsistency === 'OPTIMAL' ? 'text-emerald-400' : 'text-amber-400'}`}
                                        >
                                            {log.phenomenologicalState.internalConsistency}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="p-12 text-center border border-dashed border-white/10 rounded-xl text-gray-500">
                            No logs captured in current temporal session.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

const LogicMatrixView: React.FC = () => {
    const theme = useTheme();
    const commands = Object.values(commandRegistry);
    const focus = useCoherenceStore((state) => state.cognitiveFocus);

    return (
        <div className="space-y-8 animate-fade-in">
            <div className="p-6 bg-gradient-to-br from-indigo-900/20 to-black border border-indigo-500/20 rounded-xl">
                <div className="flex items-center gap-4 mb-6">
                    <div className="p-3 bg-indigo-500/20 rounded-lg">
                        <Brain size={24} className="text-indigo-400" />
                    </div>
                    <div>
                        <h3 className="text-2xl font-light text-indigo-100 tracking-wide">GUCA Logic Matrix</h3>
                        <p className="text-xs text-indigo-400/60 uppercase tracking-widest font-mono">
                            Governed Universal Command Architecture
                        </p>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {commands.map((cmd) => (
                        <div
                            key={cmd.commandId}
                            className="p-4 bg-black/40 border border-indigo-500/10 rounded-lg hover:bg-indigo-500/5 transition-all"
                        >
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-xs font-mono text-indigo-300">{cmd.commandId}</span>
                                <ShieldCheck size={14} className="text-indigo-500/40" />
                            </div>
                            <p className="text-xs text-indigo-200/70">{cmd.description}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-6 bg-black/30 border border-white/5 rounded-xl">
                    <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">
                        Biometric Feedback
                    </h4>
                    <SystemBiometrics />
                </div>
                <div className="p-6 bg-black/30 border border-white/5 rounded-xl flex flex-col justify-center">
                    <h4 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">Cognitive State</h4>
                    <div className="flex items-center gap-4">
                        <Activity className="text-cyan-400 animate-pulse" />
                        <div>
                            <p className="text-xs text-gray-500 uppercase">Focus Mode</p>
                            <p className="text-xl text-cyan-100 font-light">{focus}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const CognitiveProcessPage: React.FC<{ type?: 'memory' | 'logic' }> = ({ type }) => {
    const { id } = useParams<{ id: string }>();
    const theme = useTheme();

    // Prefer prop 'type', fallback to 'id' from params
    const effectiveType = type || id;
    const isMemory = effectiveType === 'memory';
    const isLogic = effectiveType === 'logic';

    return (
        <div className="p-4 md:p-8 max-w-6xl mx-auto">
            <header className="mb-10 flex items-end justify-between">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        {isMemory ? <Database className="text-cyan-400" /> : <Brain className="text-indigo-400" />}
                        <h2 className="text-3xl font-thin capitalize text-white tracking-widest">{id} Core</h2>
                    </div>
                    <p className={`text-sm text-${theme.primary}-400/60`}>
                        Sovereign Module for {id === 'memory' ? 'Archival Persistence' : 'Logic Governance'} Analysis.
                    </p>
                </div>
                <div className="hidden md:block">
                    <div
                        className={`px-4 py-1 rounded-full border border-${theme.primary}-500/20 bg-${theme.primary}-500/5 text-[10px] font-mono text-${theme.primary}-300 uppercase tracking-tighter`}
                    >
                        Module ID: MOD-PHX-{id?.toUpperCase()}
                    </div>
                </div>
            </header>

            <main>
                {isMemory && <MemoryCoreView />}
                {isLogic && <LogicMatrixView />}
                {!isMemory && !isLogic && (
                    <div className="p-20 text-center border border-dashed border-white/10 rounded-2xl text-gray-500">
                        Directives for sector "{id}" are currently restricted.
                    </div>
                )}
            </main>
        </div>
    );
};

export default CognitiveProcessPage;
