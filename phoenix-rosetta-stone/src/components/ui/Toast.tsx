import React from "react";
import { useToast } from "@/core/useToast";
import type { ToastItem } from "@/core/useToast";

export const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useToast();

  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-6 right-[300px] z-50 flex flex-col gap-3 max-w-sm pointer-events-none select-none">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className="pointer-events-auto bg-deep-space border border-celestial-blue/30 rounded p-4 shadow-float animate-toast-in flex items-start gap-3 relative overflow-hidden"
          style={{
            borderColor: toast.type === "achievement" ? "#f59e0b" : "#77b5fe",
          }}
        >
          {/* Top border ambient glow */}
          <div
            className="absolute top-0 left-0 right-0 h-[2px] opacity-65"
            style={{
              backgroundColor: toast.type === "achievement" ? "#f59e0b" : "#77b5fe",
            }}
          />

          <div className="flex-1 font-mono">
            <div className="flex items-center gap-1.5 mb-1">
              {toast.type === "achievement" ? (
                <span className="text-[10px] uppercase font-semibold text-chris-amber tracking-wider bg-chris-amber/10 border border-chris-amber/20 px-1.5 py-0.5 rounded">
                  🏆 ACHIEVEMENT SECURED
                </span>
              ) : (
                <span className="text-[10px] uppercase font-semibold text-celestial-blue tracking-wider bg-celestial-blue/10 border border-celestial-blue/20 px-1.5 py-0.5 rounded">
                  🔔 TELEMETRY NOTICE
                </span>
              )}
            </div>
            <h4 className="text-xs font-bold text-white mb-0.5 uppercase tracking-wide">
              {toast.title}
            </h4>
            <p className="text-[11px] text-white/60 leading-relaxed">
              {toast.message}
            </p>
          </div>

          <button
            onClick={() => removeToast(toast.id)}
            className="text-white/30 hover:text-white/70 cursor-pointer self-start text-xs font-semibold"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
};
