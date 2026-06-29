/**
 * @artifact packages/supabase/src/types.ts
 * @id        SYNC.SUPABASE.TYPES.001
 * @version   v1.1 [OMEGA]
 * @status    [ACTIVE]
 *
 * Supabase Database type definitions for the Synarche monorepo.
 * Derived from axion-core/supabase/migrations/ — covers all 9 migrations.
 *
 * ⚠️  To regenerate from the live remote schema, run from the workspace root:
 *     npx supabase gen types typescript \
 *       --project-id rtjkhpotguwngfpvhfej \
 *       > packages/supabase/src/types.ts
 *
 *   Or from the local Supabase instance (requires `supabase start`):
 *     cd axion-core && npx supabase gen types typescript --local \
 *       > ../packages/supabase/src/types.ts
 *
 * Tables covered (19 total across all migrations):
 *   profiles               — user auth profiles
 *   conversation_history   — Axion/Chris chat log
 *   axion_state            — persistent key/value state
 *   discovered_insights    — autonomous insight ledger
 *   notifications          — UI notification queue
 *   memory_entries         — L1-L5 cognitive memory (pgvector)
 *   memory_gems            — L1 validated insights
 *   memory_associations    — knowledge graph edges
 *   experience_logs        — immutable event chronicle
 *   episodes               — session containers
 *   axiom_knowledge        — L3-L4 long-term knowledge nodes
 *   axiom_action_log       — autonomous action accountability
 *   player_state           — RPG XP / level / prestige
 *   rpg_stats              — Celestial Chart metrics
 *   stardust_ledger        — stardust transaction audit trail
 *   achievements           — achievement definitions
 *   player_achievements    — player ↔ achievement junction
 *   knowledge_base         — general knowledge store
 *   knowledge_history      — archived knowledge snapshots
 */
export {};
//# sourceMappingURL=types.js.map