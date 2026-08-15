/**
 * @artifact src/core/hooks/useRealtime.ts
 * Generic Supabase Realtime subscription hook.
 * Powers all live-update panels in the HUD.
 */

import type { Database } from "@/core/supabase";
import { supabase } from "@/core/supabase";
import type { RealtimePostgresChangesPayload } from "@supabase/supabase-js";
import { useEffect } from "react";

type PublicTable = keyof Database["public"]["Tables"];
type RealtimeEvent = "INSERT" | "UPDATE" | "DELETE" | "*";

export function useRealtime<T extends PublicTable>(
  table: T,
  event: RealtimeEvent,
  callback: (payload: RealtimePostgresChangesPayload<Record<string, unknown>>) => void,
  enabled = true,
) {
  useEffect(() => {
    if (!enabled) return;

    const channelId = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}`;
    const channel = supabase
      .channel(`realtime:${String(table)}:${event}:${channelId}`)
      .on(
        "postgres_changes",
        { event: event as any, schema: "public", table: String(table) },
        callback,
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [table, event, enabled]); // eslint-disable-line react-hooks/exhaustive-deps
}
