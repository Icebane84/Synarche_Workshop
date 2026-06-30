import React from 'react';
import { ArrowRight, Terminal, Database, Code } from 'lucide-react';
import Tooltip from './common/Tooltip';
import { useLogStore } from '../store/logStore';

/**
 * A sub-component representing the Data Aggregator service.
 * It visualizes the collection of interaction data points.
 */
const DataAggregator: React.FC<{ isActive: boolean }> = ({ isActive }) => (
    <div className={`p-4 border rounded-lg h-full flex flex-col transition-all duration-300 cursor-pointer ${isActive ? 'bg-cyan-900/30 border-cyan-500 shadow-[0_0_15px_rgba(34,211,238,0.2)]' : 'bg-gray-900/50 border-gray-700/50 hover:bg-gray-900/80 hover:border-cyan-500/70'}`}>
        <div className="flex items-center gap-3 mb-2">
            <Database className={`w-6 h-6 transition-colors duration-300 ${isActive ? 'text-cyan-300 animate-pulse' : 'text-cyan-400'}`} />
            <h3 className="text-lg font-semibold text-cyan-200">Data Aggregator</h3>
        </div>
        <p className="text-sm text-cyan-400/80 flex-1">
            {isActive ? "Harvesting interaction metrics from active neural pathways..." : "Waiting for interaction complete event..."}
        </p>
        <div className="mt-2 h-1 w-full bg-gray-800 rounded-full overflow-hidden">
             {isActive && <div className="h-full bg-cyan-400 animate-progress-indeterminate"></div>}
        </div>
    </div>
);

/**
 * A sub-component representing the SELT Formatter engine.
 * It visualizes the structuring of aggregated data into a JSON format.
 */
const SELTFormatter: React.FC<{ isActive: boolean }> = ({ isActive }) => (
    <div className={`p-4 border rounded-lg h-full flex flex-col transition-all duration-300 cursor-pointer ${isActive ? 'bg-amber-900/30 border-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.2)]' : 'bg-gray-900/50 border-gray-700/50 hover:bg-gray-900/80 hover:border-amber-500/70'}`}>
         <div className="flex items-center gap-3 mb-2">
            <Code className={`w-6 h-6 transition-colors duration-300 ${isActive ? 'text-amber-300 animate-pulse' : 'text-amber-400'}`} />
            <h3 className="text-lg font-semibold text-cyan-200">SELT v5.1 Formatter</h3>
        </div>
        <p className="text-sm text-cyan-400/80 flex-1">
             {isActive ? "Structuring data into UMB-SELT-002 JSON schema..." : "Standby for aggregation stream..."}
        </p>
        <div className="mt-2 h-1 w-full bg-gray-800 rounded-full overflow-hidden">
             {isActive && <div className="h-full bg-amber-400 animate-progress-indeterminate" style={{ animationDelay: '0.2s'}}></div>}
        </div>
    </div>
);

const LogTerminal: React.FC = () => {
    const lastLog = useLogStore(state => state.lastLog);

    if (!lastLog) return null;

    return (
        <div className="mt-6 w-full bg-black/50 border border-cyan-500/30 rounded-lg overflow-hidden animate-fade-in-up">
            <div className="bg-gray-900/80 px-4 py-2 border-b border-cyan-500/20 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Terminal size={14} className="text-cyan-400" />
                    <span className="text-xs font-mono text-cyan-300">Omni-Log Output Stream</span>
                </div>
                <span className="text-[10px] text-cyan-500/60 font-mono">{lastLog.logId}</span>
            </div>
            <pre className="p-4 text-[10px] md:text-xs text-green-400/90 font-mono overflow-x-auto max-h-60 scrollbar-thin">
                {JSON.stringify(lastLog, null, 2)}
            </pre>
        </div>
    )
}


/**
 * A sovereign module that visually represents the fusion of the Data Aggregator
 * and SELT Formatter, forming the core of the log generation process.
 */
const MetaEngine: React.FC = () => {
  const isGenerating = useLogStore(state => state.isGenerating);

  return (
    <div className="p-6 bg-black/30 border border-cyan-500/20 rounded-lg w-full max-w-4xl mx-auto">
        <h2 className="text-2xl font-thin tracking-wider text-center text-cyan-200 drop-shadow-lg mb-6">
            SELT Meta-Engine: Log Generation Protocol
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] items-center gap-4">
            <DataAggregator isActive={isGenerating} />
            
            <div className="flex justify-center">
                <Tooltip label="Data Stream">
                    <ArrowRight className={`w-8 h-8 transition-colors duration-300 ${isGenerating ? 'text-cyan-300 animate-pulse-horizontal' : 'text-cyan-500/20'}`} />
                </Tooltip>
            </div>
            
            <SELTFormatter isActive={isGenerating} />
        </div>

        <LogTerminal />

        <style>{`
            @keyframes pulse-horizontal {
                0%, 100% { transform: scaleX(1); opacity: 0.7; }
                50% { transform: scaleX(1.1); opacity: 1; }
            }
            .animate-pulse-horizontal {
                animation: pulse-horizontal 1s infinite ease-in-out;
            }
            @keyframes progress-indeterminate {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            .animate-progress-indeterminate {
                animation: progress-indeterminate 1.5s infinite linear;
            }
             @keyframes fade-in-up {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .animate-fade-in-up { animation: fade-in-up 0.5s ease-out forwards; }
            .scrollbar-thin::-webkit-scrollbar { width: 4px; height: 4px; }
            .scrollbar-thin::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); }
            .scrollbar-thin::-webkit-scrollbar-thumb { background-color: rgba(34, 211, 238, 0.2); border-radius: 4px; }
        `}</style>
    </div>
  );
};

export default MetaEngine;