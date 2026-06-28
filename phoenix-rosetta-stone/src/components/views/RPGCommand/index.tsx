import React, { useState, useEffect } from "react";
import { useUserContext, USER_THEME } from "@/core/useUserContext";
import { usePlayerState } from "@/core/hooks/usePlayerState";
import { supabase } from "@/core/supabase";
import { StatBar } from "@/components/ui/StatBar";
import { LivePill } from "@/components/ui/LivePill";

export const RPGCommandView: React.FC = () => {
  const { userId, activeUser } = useUserContext();
  const theme = USER_THEME[activeUser];
  const { player, stats, isLoading, refetch } = usePlayerState(userId);

  // Extra data states
  const [achievements, setAchievements] = useState<any[]>([]);
  const [ledger, setLedger] = useState<any[]>([]);
  const [isUpdating, setIsUpdating] = useState(false);

  const fetchExtraData = async () => {
    // Fetch achievements
    const achs = await supabase.from("achievements").select("*").order("created_at", { ascending: false });
    setAchievements(achs.data ?? []);

    // Fetch stardust ledger
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

  // Actions
  const handleAddXp = async () => {
    if (!player) return;
    setIsUpdating(true);
    const addedXp = 250;
    let newXp = (player.xp ?? 0) + addedXp;
    let newLevel = player.level ?? 1;
    const nextLevelXp = newLevel * 1000;

    if (newXp >= nextLevelXp) {
      newXp -= nextLevelXp;
      newLevel += 1;
    }

    await supabase
      .from("player_state")
      .update({ xp: newXp, level: newLevel })
      .eq("user_id", userId);

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

    // 1. Update player stardust
    await supabase
      .from("player_state")
      .update({ stardust: (player.stardust ?? 0) + amount })
      .eq("user_id", userId);

    // 2. Log in ledger
    await supabase.from("stardust_ledger").insert({
      user_id: userId,
      amount,
      transaction_type: "EARNED",
      target_stat: "stardust",
      reference_impact_id: "manual_hack",
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
        {/* Left Side: Stats Radar / List */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono">
            COGNITIVE ATTRIBUTES
          </h3>

          <div className="bg-panel-bg/40 border border-white/5 rounded-lg p-5 space-y-4">
            {isLoading ? (
              <div className="py-8 text-center text-xs text-white/30 animate-pulse font-mono">
                Calculating stat modifiers...
              </div>
            ) : !stats ? (
              <div className="py-8 text-center text-xs text-white/30 italic font-mono">
                No attributes found for current entity.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <StatBar
                    label="Coherence Index"
                    value={stats.coherence ?? 0}
                    colorClass="bg-coherence-indigo"
                  />
                  <StatBar
                    label="Synergy Rate"
                    value={stats.synergy ?? 0}
                    colorClass="bg-synergy-emerald"
                  />
                  <StatBar
                    label="Adaptability Matrix"
                    value={stats.adaptability ?? 0}
                    colorClass="bg-adapt-amber"
                  />
                  <StatBar
                    label="Transparency Coefficient"
                    value={stats.transparency ?? 0}
                    colorClass="bg-transparency-silver"
                  />
                </div>
                <div className="space-y-4">
                  <StatBar
                    label="Ascension Level"
                    value={stats.form_ascension ?? 0}
                    colorClass="bg-form-ascension"
                  />
                  <StatBar
                    label="Semantic Friction"
                    value={stats.semantic_friction ?? 0}
                    colorClass="bg-semantic-friction"
                  />
                  <StatBar
                    label="Creative Spark"
                    value={stats.creative_spark ?? 0}
                    colorClass="bg-creative-spark"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Stardust Ledger */}
          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono pt-2">
            STARDUST TRANSACTION LEDGER
          </h3>
          <div className="bg-panel-bg/40 border border-white/5 rounded-lg p-4 font-mono text-xs overflow-x-auto">
            <table className="w-full text-left">
               <thead>
                <tr className="border-b border-white/10 text-chrome">
                  <th className="pb-2">Time</th>
                  <th className="pb-2">Amount</th>
                  <th className="pb-2">Type</th>
                  <th className="pb-2">Reference</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-white/70">
                {ledger.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="py-4 text-center text-white/30 italic">
                      No stardust events recorded.
                    </td>
                  </tr>
                ) : (
                  ledger.map((item) => (
                    <tr key={item.id} className="hover:bg-white/[0.01]">
                      <td className="py-2.5 text-[10px] text-white/40">
                        {item.created_at ? new Date(item.created_at).toLocaleTimeString() : "00:00"}
                      </td>
                      <td className={`py-2.5 font-bold ${item.amount >= 0 ? "text-green-400" : "text-red-400"}`}>
                        {item.amount >= 0 ? `+${item.amount}` : item.amount}
                      </td>
                      <td className="py-2.5">{item.transaction_type}</td>
                      <td className="py-2.5 text-white/50">{item.reference_impact_id || "Direct Hack"}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Side: Player Profile & Achievements */}
        <div className="space-y-4">
          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono">
            PLAYER PROFILE
          </h3>

          <div className="bg-panel-bg/40 border border-white/5 rounded-lg p-4 font-mono text-xs space-y-3">
            <div className="flex justify-between">
              <span className="text-white/40">User Identity:</span>
              <span className="text-white font-bold" style={{ color: theme.accent }}>
                {activeUser}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/40">Prestige Rank:</span>
              <span className="text-white">Alpha Master</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/40">Coherence:</span>
              <span className="text-white">{stats?.coherence ?? 0}%</span>
            </div>
          </div>

          <h3 className="text-xs font-semibold tracking-[0.25em] text-white/60 uppercase font-mono pt-2">
            ACHIEVEMENTS SECURED
          </h3>

          <div className="space-y-3">
            {achievements.length === 0 ? (
              <div className="bg-panel-bg/25 border border-white/5 p-6 rounded-lg text-center text-xs text-white/30 italic font-mono">
                No achievements unlocked yet.
              </div>
            ) : (
              achievements.map((ach) => (
                <div
                  key={ach.id}
                  className="bg-panel-bg/40 border border-white/5 rounded-lg p-3 font-mono text-xs flex gap-3 relative overflow-hidden"
                >
                  <div className="text-xl">🏆</div>
                  <div>
                    <h4 className="font-bold text-white/95">{ach.title || "First Steps"}</h4>
                    <p className="text-[10px] text-white/50">{ach.description || "Initialize the Phoenix core."}</p>
                    <div className="text-[9px] text-chris-amber font-semibold mt-1">
                      +1,000 XP • +100 Stardust
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
