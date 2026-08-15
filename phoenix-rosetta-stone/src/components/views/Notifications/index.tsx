import React from "react";
import { useNotifications } from "@/core/hooks/useNotifications";
import { LivePill } from "@/components/ui/LivePill";

export const NotificationsView: React.FC = () => {
  const { notifications, unreadCount, isLoading, markRead, markAllRead } = useNotifications();

  return (
    <div className="space-y-6 animate-appear">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase">
            NOTIFICATIONS FEED
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">
            Operational alerts, achievement unlocks, and cognitive updates
          </p>
        </div>
        <div className="flex items-center gap-3">
          {unreadCount > 0 && (
            <button
              onClick={markAllRead}
              className="px-3 py-1 bg-white/5 hover:bg-white/10 border border-white/10 rounded font-mono text-[10px] text-white/70 hover:text-white transition-all cursor-pointer"
            >
              MARK ALL READ ({unreadCount})
            </button>
          )}
        </div>
      </div>

      <div className="max-w-3xl mx-auto space-y-4">
        {isLoading ? (
          <div className="text-center py-12 text-xs text-white/30 animate-pulse font-mono">
            Accessing notification logs...
          </div>
        ) : notifications.length === 0 ? (
          <div className="bg-panel-bg/25 border border-white/5 p-8 rounded-lg text-center text-xs text-white/30 italic font-mono">
            No telemetry notifications recorded.
          </div>
        ) : (
          <div className="space-y-3">
            {notifications.map((notif, idx) => (
              <div
                key={notif.id || `notif-${idx}`}
                className={`bg-panel-bg/40 border p-4 rounded-lg font-mono text-xs flex items-start gap-4 transition-all duration-300 ${
                  notif.read ? "border-white/5 opacity-70" : "border-celestial-blue/30 shadow-[0_0_10px_rgba(119,181,254,0.05)]"
                }`}
              >
                {/* Unread indicator dot */}
                <div className="pt-1.5">
                  <span
                    className={`block w-2.5 h-2.5 rounded-full ${
                      notif.read ? "bg-white/10" : "bg-celestial-blue animate-pulse shadow-[0_0_8px_#77b5fe]"
                    }`}
                  />
                </div>

                {/* Content */}
                <div className="flex-1 space-y-1">
                  <div className="flex items-center justify-between gap-4">
                    <span className="font-bold text-white/95 text-xs">{notif.title || "Telemetry Alert"}</span>
                    <span className="text-[10px] text-white/30">
                      {notif.created_at ? new Date(notif.created_at).toLocaleString() : ""}
                    </span>
                  </div>
                  <p className="text-white/60 font-sans text-xs select-text">{notif.message}</p>
                </div>

                {/* Mark as read action */}
                {!notif.read && (
                  <button
                    onClick={() => markRead(notif.id)}
                    className="px-2.5 py-1 border border-white/10 rounded hover:border-celestial-blue/50 bg-white/5 hover:bg-celestial-blue/10 text-[10px] text-white/40 hover:text-celestial-blue transition-colors cursor-pointer"
                  >
                    Mark Read
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
