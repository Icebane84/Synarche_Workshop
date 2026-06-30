import React from "react";
import { Menu, Zap, Command, Wifi, WifiOff, Database, Activity } from "lucide-react";
import { useUIStore } from "../store/uiStore";
import { useTheme } from "../hooks/useTheme";
import { useFileSystemStore } from "../store/fileSystemStore";
import { useTaskStore } from "../store/taskStore";
import { useCoherenceStore } from "../store/coherenceStore";
import Tooltip from "./common/Tooltip";

interface HeaderProps {
    onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
    const theme = useTheme();
    const toggleSynapse = useUIStore((state) => state.toggleSynapse);
    const isLocalConnected = useFileSystemStore((state) => state.isConnected);
    const { isSimulationMode, connectionStatus, initialize: initializeTasks } = useTaskStore();
    const { maintenanceMode, setMaintenanceMode } = useCoherenceStore();

    return (
        <header
            className={`flex items-center justify-between px-6 py-3 border-b border-${theme.primary}-500/20 bg-black/40 backdrop-blur-md z-40`}
        >
            {/* Left: Logo & Menu */}
            <div className="flex items-center gap-4">
                <button
                    onClick={onMenuClick}
                    className={`md:hidden p-2 text-${theme.primary}-400 hover:bg-${theme.primary}-500/10 rounded-md transition-colors`}
                >
                    <Menu size={20} />
                </button>
                <div className="flex items-center gap-3">
                    <div
                        className={`p-2 bg-${theme.primary}-500/10 rounded-lg border border-${theme.primary}-500/20 shadow-[0_0_15px_-3px_rgba(34,211,238,0.2)]`}
                    >
                        <Zap className={`w-5 h-5 text-${theme.primary}-400`} />
                    </div>
                    <div>
                        <h1
                            className={`font-holographic text-lg tracking-wider text-${theme.primary}-100 leading-none`}
                        >
                            ROSETTA <span className={`text-${theme.primary}-500/80`}>STONE</span>
                        </h1>
                        <p className={`text-[10px] uppercase tracking-[0.2em] text-${theme.primary}-400/50 font-mono`}>
                            Phoenix Protocol v10.0
                        </p>
                    </div>
                </div>
            </div>

            {/* Center: Synapse Trigger (Desktop) */}
            <div className="hidden md:flex items-center">
                <button
                    onClick={toggleSynapse}
                    className={`group flex items-center gap-3 px-4 py-2 bg-black/40 border border-${theme.primary}-500/30 rounded-full hover:bg-${theme.primary}-500/10 hover:border-${theme.primary}-500/50 transition-all duration-300 shadow-lg`}
                >
                    <Command size={14} className={`text-${theme.primary}-400 group-hover:text-${theme.primary}-200`} />
                    <span
                        className={`text-xs font-mono text-${theme.primary}-300/70 group-hover:text-${theme.primary}-200`}
                    >
                        Initialize Synapse...
                    </span>
                    <span
                        className={`text-[10px] px-1.5 py-0.5 rounded bg-${theme.primary}-500/20 text-${theme.primary}-400/80 border border-${theme.primary}-500/20`}
                    >
                        ⌘K
                    </span>
                </button>
            </div>

            {/* Right: Status Indicators */}
            <div className="flex items-center gap-4">
                {/* Neural Link Status */}
                <Tooltip label={isLocalConnected ? "Neural Link Active" : "Neural Link Offline"}>
                    <div
                        className={`hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full border ${
                            isLocalConnected
                                ? `bg-emerald-500/5 border-emerald-500/20`
                                : `bg-rose-500/5 border-rose-500/10`
                        }`}
                    >
                        {isLocalConnected ? (
                            <Wifi size={14} className="text-emerald-400" />
                        ) : (
                            <WifiOff size={14} className="text-rose-500/50" />
                        )}
                        <span
                            className={`text-[10px] font-mono tracking-wider ${
                                isLocalConnected ? "text-emerald-400/80" : "text-rose-500/40"
                            }`}
                        >
                            NEURAL
                        </span>
                    </div>
                </Tooltip>

                {/* Sovereign Link Status */}
                <Tooltip label={
                    connectionStatus === 'connected' ? "Sovereign Uplink Established" :
                    connectionStatus === 'connecting' ? "Establishing Neural Handshake..." :
                    connectionStatus === 'degraded' ? "Handshake Dissonance: Simulation Active" :
                    "Sovereign Uplink Offline"
                }>
                    <button
                        onClick={() => initializeTasks()}
                        disabled={connectionStatus === 'connecting'}
                        className={`hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all duration-300 active:scale-95 ${
                            connectionStatus === 'connected' ? `bg-indigo-500/10 border-indigo-500/40 shadow-[0_0_10px_rgba(99,102,241,0.2)]` :
                            connectionStatus === 'connecting' ? `bg-blue-500/10 border-blue-500/40 animate-pulse` :
                            connectionStatus === 'degraded' ? `bg-amber-500/10 border-amber-500/40` :
                            `bg-rose-500/10 border-rose-500/40`
                        }`}
                    >
                        <Database 
                            size={14} 
                            className={`
                                ${connectionStatus === 'connected' ? "text-indigo-400" : 
                                  connectionStatus === 'connecting' ? "text-blue-400 animate-spin" : 
                                  connectionStatus === 'degraded' ? "text-amber-400" : 
                                  "text-rose-400"}
                            `} 
                        />
                        <span
                            className={`text-[10px] font-mono tracking-wider ${
                                connectionStatus === 'connected' ? "text-indigo-400" : 
                                connectionStatus === 'connecting' ? "text-blue-400" : 
                                connectionStatus === 'degraded' ? "text-amber-400" : 
                                "text-rose-400"
                            }`}
                        >
                            {connectionStatus === 'connected' ? "SOVEREIGN" : 
                             connectionStatus === 'connecting' ? "SYNCING..." : 
                             connectionStatus === 'degraded' ? "DEGRADED" : 
                             "OFFLINE"}
                        </span>
                    </button>
                </Tooltip>

                {/* Maintenance Mode Toggle */}
                <Tooltip label={`Protocol Maintenance: ${maintenanceMode} Mode`}>
                    <select
                        value={maintenanceMode}
                        onChange={(e) => {
                            setMaintenanceMode(e.target.value as any);
                        }}
                        className={`hidden lg:block bg-black/40 border border-${theme.primary}-500/20 text-[9px] font-mono uppercase tracking-widest px-2 py-1.5 rounded-full focus:outline-none hover:bg-${theme.primary}-500/10 transition-colors cursor-pointer text-${theme.primary}-400`}
                    >
                        <option value="Manual">Manual</option>
                        <option value="Permissioned">Permissioned</option>
                        <option value="Sovereign">Sovereign</option>
                    </select>
                </Tooltip>

                <div
                    className={`w-8 h-8 rounded-full bg-gradient-to-tr from-${theme.primary}-500/20 to-${theme.secondary}-500/20 border border-${theme.primary}-500/30 flex items-center justify-center`}
                >
                    <Activity size={16} className={`text-${theme.primary}-400 animate-pulse-slow`} />
                </div>
            </div>
        </header>
    );
};

export default Header;
