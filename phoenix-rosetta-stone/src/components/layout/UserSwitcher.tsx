import React from "react";
import { useUserContext, USER_THEME } from "@/core/useUserContext";

export const UserSwitcher: React.FC = () => {
  const { activeUser, setUser } = useUserContext();

  return (
    <div className="flex items-center gap-2 bg-panel-bg border border-white/5 rounded-md p-1 font-mono text-xs">
      <span className="text-chrome pl-1 mr-1">Identity:</span>
      <button
        onClick={() => setUser("Chris")}
        className={`px-3 py-1 rounded transition-all duration-200 cursor-pointer ${
          activeUser === "Chris"
            ? "bg-chris-amber/10 border border-chris-amber/40 text-chris-amber shadow-glow-amber font-semibold"
            : "border border-transparent text-white/40 hover:text-white/80 hover:bg-white/5"
        }`}
      >
        CHRIS
      </button>
      <button
        onClick={() => setUser("Axion")}
        className={`px-3 py-1 rounded transition-all duration-200 cursor-pointer ${
          activeUser === "Axion"
            ? "bg-axion-indigo/10 border border-axion-indigo/40 text-axion-indigo shadow-glow-indigo font-semibold"
            : "border border-transparent text-white/40 hover:text-white/80 hover:bg-white/5"
        }`}
      >
        AXION
      </button>
    </div>
  );
};
