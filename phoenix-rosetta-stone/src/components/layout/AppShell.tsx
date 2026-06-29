import React, { useEffect } from "react";
import { Sidebar } from "./Sidebar";
import { ActivityRail } from "./ActivityRail";
import { UserSwitcher } from "./UserSwitcher";
import { useUserContext, USER_THEME } from "@/core/useUserContext";
import { useToast } from "@/components/ui/Toast";
import { NexusSignalBusClient, NexusSignalEnvelope } from "@synarche/nexus-signalbus";

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const { activeUser } = useUserContext();
  const { addToast } = useToast();
  const theme = USER_THEME[activeUser];

  useEffect(() => {
    const bus = new NexusSignalBusClient("phoenix-rosetta-stone");
    const unsubscribe = bus.subscribe((signal: NexusSignalEnvelope) => {
      if (signal.sourceApp !== "phoenix-rosetta-stone") {
        if (signal.action === "ASCEND_ERA") {
          addToast({
            title: "🌟 NEXUS SIGNAL RECEIVED",
            message: `[${signal.sourceApp}] Species ascended to ${signal.payload.nextStage} Era! (+250 RPG XP)`,
            type: "info",
          });
        } else if (signal.action === "COLONIZE_PLANET") {
          addToast({
            title: "🚀 NEXUS SIGNAL RECEIVED",
            message: `[${signal.sourceApp}] Established outpost on ${signal.payload.planetName}! (+100 RPG XP)`,
            type: "info",
          });
        }
      }
    });

    return () => {
      unsubscribe();
      bus.close();
    };
  }, [addToast]);

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
            {/* Identity Switcher */}
            <UserSwitcher />
          </div>
        </header>

        {/* View Content Area */}
        <main className="flex-1 overflow-y-auto relative p-6 scrollbar-thin">
          {children}
        </main>
      </div>

      {/* Activity stream rail (Right) */}
      <ActivityRail />
    </div>
  );
};
