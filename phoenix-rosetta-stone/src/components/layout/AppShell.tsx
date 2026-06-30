import { ActivityRail } from "@components/layout/ActivityRail";
import { Sidebar } from "@components/layout/Sidebar";
import { TheSynapse } from "@components/layout/TheSynapse";
import { UserSwitcher } from "@components/layout/UserSwitcher";
import { useToast } from "@core/useToast";
import { useUserContext } from "@core/useUserContext";
import {
    type AscendEraPayload,
    type ColonizePlanetPayload,
    type MissionCompletePayload,
    NexusSignalBusClient,
} from "@synarche/nexus-signalbus";
import React, { useEffect, useState } from "react";

interface AppShellProps {
    children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
    const { activeUser } = useUserContext();
    const { addToast } = useToast();
    const [isSynapseOpen, setIsSynapseOpen] = useState(false);

    useEffect(() => {
        const bus = new NexusSignalBusClient("phoenix-rosetta-stone");
        const unsubscribe = bus.subscribe((signal) => {
            if (signal.sourceApp !== "phoenix-rosetta-stone") {
                switch (signal.action) {
                    case "ASCEND_ERA": {
                        const payload = signal.payload as AscendEraPayload;
                        addToast({
                            title: "🌟 NEXUS SIGNAL RECEIVED",
                            message: `[${signal.sourceApp}] Species ascended to ${payload.nextStage} Era! (+250 RPG XP)`,
                            type: "achievement",
                        });
                        break;
                    }
                    case "COLONIZE_PLANET": {
                        const payload = signal.payload as ColonizePlanetPayload;
                        addToast({
                            title: "🚀 NEXUS SIGNAL RECEIVED",
                            message: `[${signal.sourceApp}] Established outpost on ${payload.planetName}! (+100 RPG XP)`,
                            type: "achievement",
                        });
                        break;
                    }
                    case "MISSION_COMPLETE": {
                        const payload = signal.payload as MissionCompletePayload;
                        addToast({
                            title: "🛡️ MISSION COMPLETE",
                            message: `[${signal.sourceApp}] Completed: ${payload.missionName}! (+${payload.xpReward} RPG XP)`,
                            type: "achievement",
                        });
                        break;
                    }
                }
            }
        });

        return () => {
            unsubscribe();
            bus.close();
        };
    }, [addToast]);

    // Hotkey listener for Ctrl + `
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.ctrlKey && e.key === "`") {
                e.preventDefault();
                setIsSynapseOpen((prev) => !prev);
            }
        };
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, []);

    return (
        <div className="flex w-screen h-screen overflow-hidden bg-nebula-void text-white font-sans">
            {/* Sidebar (Left) */}
            <Sidebar />

            {/* Main Layout Area (Center) */}
            <div className="flex-1 flex flex-col min-w-0 bg-deep-space relative">
                {/* Main Header */}
                <header className="h-14 px-6 border-b border-white/5 flex items-center justify-between z-10 select-none">
                    <div className="flex items-center gap-4">
                        <h1 className="text-sm font-semibold tracking-[0.25em] text-white flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                            SYNARCHE MASTER OVERLAY
                        </h1>
                        <span className="text-[10px] bg-white/5 border border-white/10 px-2 py-0.5 rounded text-white/50 font-mono">
                            SUBSTRATE COMPILATION
                        </span>
                    </div>

                    <div className="flex items-center gap-4">
                        {/* Terminal Button */}
                        <button
                            onClick={() => setIsSynapseOpen(true)}
                            className="p-1.5 rounded bg-white/5 border border-white/10 text-white/60 hover:text-white hover:bg-white/10 transition-colors font-mono text-xs cursor-pointer"
                            title="Open Synapse Command Console (Ctrl + `)"
                        >
                            [ &gt;_ ]
                        </button>

                        {/* Identity Switcher */}
                        <UserSwitcher />
                    </div>
                </header>

                {/* View Content Area */}
                <main className="flex-1 overflow-y-auto relative p-6 scrollbar-thin">{children}</main>
            </div>

            {/* Activity stream rail (Right) */}
            <ActivityRail />

            {/* Command Terminal Overlay */}
            <TheSynapse isOpen={isSynapseOpen} onClose={() => setIsSynapseOpen(false)} />
        </div>
    );
};
