/**
 * @artifact src/core/hooks/useActionLog.ts
 * @relations
 * REF: useMemoryFeed.ts
 * REF: useNotifications.ts
 * Live-streaming axiom_action_log — the HUD's activity ticker.
 */

import { useState, useCallback, useEffect } from "react";
import { supabase } from "@/core/supabase";
import { useRealtime } from "./useRealtime";
import type { Tables } from "@/core/supabase";

type ActionLogEntry = Tables<"axiom_action_log">;

interface UseActionLogResult {
  entries: ActionLogEntry[];
  isLoading: boolean;
  error: string | null;
}

const MAX_ENTRIES = 50;

export function useActionLog(): UseActionLogResult {
  const [entries, setEntries] = useState<ActionLogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initial load — last 50 entries
  const fetch = useCallback(async () => {
    const { data, error: err } = await supabase
      .from("axiom_action_log")
      .select("*")
      .order("timestamp", { ascending: false })
      .limit(MAX_ENTRIES);

    if (err) setError(err.message);
    else setEntries(data ?? []);
    setIsLoading(false);
  }, []);

  // Run once on mount
  useEffect(() => {
    fetch();
  }, [fetch]);

  // Stream new entries in real-time
  useRealtime("axiom_action_log", "INSERT", (payload) => {
    const newEntry = payload.new as ActionLogEntry;
    setEntries((prev) => [newEntry, ...prev.slice(0, MAX_ENTRIES - 1)]);
  });

  return { entries, isLoading, error };
}
