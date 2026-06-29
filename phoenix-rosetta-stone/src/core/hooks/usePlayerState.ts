/**
 * @artifact src/core/hooks/usePlayerState.ts
 * Live RPG player state — player_state + rpg_stats with Realtime.
 */

import { useState, useEffect, useCallback } from "react";
import { supabase } from "@/core/supabase";
import { useRealtime } from "./useRealtime";
import type { PlayerState, RpgStats } from "@/core/supabase";

interface UsePlayerStateResult {
  player: PlayerState | null;
  stats: RpgStats | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => void;
}

export function usePlayerState(userId: string): UsePlayerStateResult {
  const [player, setPlayer] = useState<PlayerState | null>(null);
  const [stats, setStats] = useState<RpgStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    const [playerRes, statsRes] = await Promise.all([
      supabase.from("player_state").select("*").eq("user_id", userId).maybeSingle(),
      supabase.from("rpg_stats").select("*").eq("user_id", userId).maybeSingle(),
    ]);

    if (playerRes.error) {
      setError(playerRes.error.message);
    } else {
      setPlayer(playerRes.data ?? null);
    }

    if (statsRes.error) {
      setError(statsRes.error.message);
    } else {
      setStats(statsRes.data ?? null);
    }

    setIsLoading(false);
  }, [userId]);

  useEffect(() => { fetch(); }, [fetch]);

  // Live update when rpg_stats changes for this user
  useRealtime("rpg_stats", "UPDATE", (payload) => {
    const updated = payload.new as RpgStats;
    if (updated.user_id === userId) {
      setStats(updated);
    }
  });

  // Live update when player_state changes
  useRealtime("player_state", "UPDATE", (payload) => {
    const updated = payload.new as PlayerState;
    if (updated.user_id === userId) {
      setPlayer(updated);
    }
  });

  return { player, stats, isLoading, error, refetch: fetch };
}
