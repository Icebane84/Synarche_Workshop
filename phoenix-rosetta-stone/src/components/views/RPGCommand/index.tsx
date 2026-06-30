import React, { useState, useEffect } from "react";
import { useUserContext, USER_THEME } from "@/core/useUserContext";
import { usePlayerState } from "@/core/hooks/usePlayerState";
import { supabase } from "@/core/supabase";
import { AttributesPanel } from "./AttributesPanel";
import { StardustLedger } from "./StardustLedger";
import { AchievementsPanel } from "./AchievementsPanel";

export const RPGCommandView: React.FC = () => {
  const { userId, activeUser } = useUserContext();
  const theme = USER_THEME[activeUser];
  const { player, stats, isLoading, refetch } = usePlayerState(userId);

  const [achievements, setAchievements] = useState<any[]>([]);
  const [ledger, setLedger] = useState<any[]>([]);
  const [isUpdating, setIsUpdating] = useState(false);

  const fetchExtraData = async () => {
    const achs = await supabase.from("achievements").select("*").order("created_at", { ascending: false });
    setAchievements(achs.data ?? []);

    const ledg = await supabase
      .from("stardust_ledger")
      .select("*")
      .eq("user_id", userId)
      .order("created_at", { ascending: false })
      .limit(10);
    setLedger(ledg.data ?? []);
  };

  useEffect(() => {
    fetchExtraData();
  }, [userId]);

  const handleAddXp = async () => {
    if (!player) return;
    setIsUpdating(true);
    const addedXp = 250;
    let newXp = (player.xp ?? 0) + addedXp;
    let newLevel = player.level ?? 1;
    const nextLevelXp = newLevel * 1000;

    if (newXp >= nextLevelXp) { newXp -= nextLevelXp; newLevel += 1; }

    await supabase.from("player_state").update({ xp: newXp, level: newLevel }).eq("user_id", userId);
    await supabase.from("axiom_action_log").insert({
      action_type: "XP_AWARD",
      details: `Awarded ${addedXp} XP to ${activeUser}. Total Level: ${newLevel}`,
      triggered_by: activeUser,
    });
    refetch();
    setIsUpdating(false);
  };

  const handleAddStardust = async () => {
    if (!player) return;
    setIsUpdating(true);
    const amount = 50;

    await supabase
      .from("player_stats")
      .update({ stardust_available: (stats?.stardust_available ?? 0) + amount })
      .eq("user_id", userId);

    await supabase.from("stardust_ledger").insert({
      user_id: userId, amount, transaction_type: "EARNED",
      target_stat: "stardust", reference_impact_id: "manual_hack",
    });

    await supabase.from("axiom_action_log").insert({
      action_type: "STARDUST_INJECTION",
      details: `Injected ${amount} stardust into ${activeUser}'s core.`,
      triggered_by: activeUser,
    });

    refetch();
    fetchExtraData();
    setIsUpdating(false);
  };

  return (
    <div className="space-y-6 animate-appear">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="text-sm font-bold tracking-[0.25em] text-white uppercase">
            RPG COMMAND INTERFACE
          </h2>
          <p className="text-[11px] text-white/40 font-mono mt-0.5">
            Sovereign stats scaling, achievement logs, and stardust ledger balance
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleAddXp}
            disabled={isUpdating}
            className="px-3 py-1 bg-white/5 hover:bg-white/10 border border-white/10 rounded font-mono text-[10px] text-white/70 hover:text-white transition-all cursor-pointer"
          >
            +250 XP
          </button>
          <button
            onClick={handleAddStardust}
            disabled={isUpdating}
            className="px-3 py-1 bg-celestial-blue/10 hover:bg-celestial-blue/20 border border-celestial-blue/30 rounded font-mono text-[10px] text-celestial-blue transition-all cursor-pointer"
          >
            +50 STARDUST
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Attributes & Ledger */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono">
            COGNITIVE ATTRIBUTES
          </h3>
          <div className="bg-panel-bg/40 border border-white/5 rounded-lg p-5 space-y-4">
            <AttributesPanel stats={stats} isLoading={isLoading} />
          </div>

          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono pt-2">
            STARDUST TRANSACTION LEDGER
          </h3>
          <StardustLedger ledger={ledger} />
        </div>

        {/* Right: Player Profile & Achievements */}
        <div className="space-y-4">
          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono">
            PLAYER PROFILE
          </h3>
          <div className="bg-panel-bg/40 border border-white/5 rounded-lg p-4 font-mono text-xs space-y-3">
            <div className="flex justify-between">
              <span className="text-white/40">User Identity:</span>
              <span className="text-white font-bold" style={{ color: theme.accent }}>{activeUser}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/40">Prestige Rank:</span>
              <span className="text-white">Alpha Master</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/40">Coherence:</span>
              <span className="text-white">{stats?.coherence_index ?? 0}%</span>
            </div>
          </div>

          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono pt-2">
            ACHIEVEMENTS SECURED
          </h3>
          <AchievementsPanel achievements={achievements} />
        </div>
      </div>
    </div>
  );
};
