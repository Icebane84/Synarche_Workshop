import React, { useState } from "react";
import { Link as LinkIcon, Unplug, RefreshCw, AlertCircle, Loader, Database } from "lucide-react";
import Tooltip from "../common/Tooltip";
import { useFileSystemStore } from "../../store/fileSystemStore";
import { useTaskStore } from "../../store/taskStore";
import { useTheme } from "../../hooks/useTheme";
import { dispatchCommand, initiateAutoRepairCommand, connectLocalFsCommand } from "../../services";

const ConnectivityStatus: React.FC = () => {
    const isLocalConnected = useFileSystemStore((state) => state.isConnected);
    const projectName = useFileSystemStore((state) => state.projectName);
    const isSimulationMode = useTaskStore((state) => state.isSimulationMode);
    const backendError = useTaskStore((state) => state.error);
    const isSyncing = useTaskStore((state) => state.isLoading);
    const theme = useTheme();
    const [isLinking, setIsLinking] = useState(false);

    const handleRepair = async () => {
        await dispatchCommand(initiateAutoRepairCommand, {});
    };

    const handleConnectNeural = async () => {
        setIsLinking(true);
        await dispatchCommand(connectLocalFsCommand, {});
        setIsLinking(false);
    };

    return (
        <div className={`px-4 py-3 border-t border-${theme.primary}-500/10 space-y-4`}>
            {/* Neural Link (Local FS) */}
            <div>
                <div className="flex items-center justify-between text-[10px] mb-1.5">
                    <span className={`text-${theme.primary}-400/60 font-semibold tracking-widest uppercase`}>
                        Neural Link
                    </span>
                    <div className="flex items-center gap-2">
                        {isLocalConnected ? (
                            <div className="flex items-center gap-1 text-emerald-400 font-bold">ACTIVE</div>
                        ) : (
                            <div className="flex items-center gap-1 text-gray-500">OFFLINE</div>
                        )}
                        {!isLocalConnected && (
                            <Tooltip label="Bridge Neural Link (Direct Restoration)">
                                <button
                                    onClick={handleConnectNeural}
                                    disabled={isLinking}
                                    className={`p-1 rounded-md bg-cyan-500/10 border border-cyan-500/20 hover:bg-cyan-500/20 transition-all ${
                                        isLinking
                                            ? "text-cyan-400 animate-pulse"
                                            : "text-cyan-400/70 hover:text-cyan-200"
                                    }`}
                                >
                                    {isLinking ? <Loader size={10} className="animate-spin" /> : <Unplug size={10} />}
                                </button>
                            </Tooltip>
                        )}
                    </div>
                </div>
                <button
                    onClick={!isLocalConnected ? handleConnectNeural : undefined}
                    disabled={isLinking}
                    className={`w-full flex items-center gap-2 px-2 py-1.5 bg-black/20 rounded border border-${
                        theme.primary
                    }-500/10 truncate transition-all duration-500 ${
                        !isLocalConnected
                            ? "hover:bg-cyan-500/5 hover:border-cyan-500/30 cursor-pointer"
                            : "cursor-default"
                    }`}
                >
                    <LinkIcon
                        size={10}
                        className={isLocalConnected ? `text-emerald-400 animate-pulse` : `text-gray-500`}
                    />
                    <span
                        className={`text-[10px] font-mono truncate ${
                            isLocalConnected ? `text-${theme.primary}-200` : `text-gray-500 italic`
                        }`}
                    >
                        {isLocalConnected ? projectName || "Active Node" : "Establish Bridge..."}
                    </span>
                </button>
            </div>

            {/* Sovereign Link (Supabase) */}
            <div>
                <div className="flex items-center justify-between text-[10px] mb-1.5">
                    <span className={`text-${theme.primary}-400/60 font-semibold tracking-widest uppercase`}>
                        Sovereign Link
                    </span>
                    <div className="flex items-center gap-2">
                        {!isSimulationMode ? (
                            <div className="flex items-center gap-1 text-emerald-400 font-bold">ACTIVE</div>
                        ) : (
                            <div className="flex items-center gap-1 text-amber-500">SIMULATED</div>
                        )}
                        {(backendError || isSimulationMode) && (
                            <Tooltip label="Trigger Autonomic Repair Sequence">
                                <button
                                    onClick={handleRepair}
                                    disabled={isSyncing}
                                    className={`p-1 rounded-md bg-amber-500/10 border border-amber-500/20 hover:bg-amber-500/20 transition-all ${
                                        isSyncing
                                            ? "text-cyan-400 animate-spin"
                                            : "text-amber-500/70 hover:text-amber-400"
                                    }`}
                                >
                                    <RefreshCw size={10} />
                                </button>
                            </Tooltip>
                        )}
                    </div>
                </div>
                <div
                    className={`flex items-center gap-2 px-2 py-1.5 bg-black/20 rounded border border-${theme.primary}-500/10 transition-all duration-500`}
                >
                    <Database size={10} className={!isSimulationMode ? `text-emerald-400` : `text-amber-500/50`} />
                    <span
                        className={`text-[10px] font-mono ${
                            !isSimulationMode ? `text-${theme.primary}-200` : `text-gray-500`
                        }`}
                    >
                        {!isSimulationMode ? "Supabase Primary" : "Local RAM Buffer"}
                    </span>
                </div>
                {backendError && (
                    <div className="mt-1.5 flex items-start gap-1.5 px-2 py-1 bg-rose-500/5 border border-rose-500/10 rounded">
                        <AlertCircle size={10} className="text-rose-400 mt-0.5 shrink-0" />
                        <span className="text-[9px] text-rose-300/70 leading-tight">
                            Handshake Dissonance: {backendError}
                        </span>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ConnectivityStatus;
