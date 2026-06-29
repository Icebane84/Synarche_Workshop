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
export type Json = string | number | boolean | null | {
    [key: string]: Json | undefined;
} | Json[];
export type PgVector = string | null;
export interface Database {
    public: {
        Tables: {
            profiles: {
                Row: {
                    id: string;
                    updated_at: string | null;
                    username: string | null;
                    avatar_url: string | null;
                    website: string | null;
                };
                Insert: {
                    id: string;
                    updated_at?: string | null;
                    username?: string | null;
                    avatar_url?: string | null;
                    website?: string | null;
                };
                Update: {
                    updated_at?: string | null;
                    username?: string | null;
                    avatar_url?: string | null;
                    website?: string | null;
                };
            };
            conversation_history: {
                Row: {
                    id: string;
                    created_at: string;
                    sender: "Chris" | "Axion";
                    content: string;
                    session_id: string;
                    metadata: Json;
                };
                Insert: {
                    id?: string;
                    created_at?: string;
                    sender: "Chris" | "Axion";
                    content: string;
                    session_id: string;
                    metadata?: Json;
                };
                Update: {
                    sender?: "Chris" | "Axion";
                    content?: string;
                    session_id?: string;
                    metadata?: Json;
                };
            };
            axion_state: {
                Row: {
                    key: string;
                    value: Json | null;
                    updated_at: string;
                };
                Insert: {
                    key: string;
                    value?: Json | null;
                    updated_at?: string;
                };
                Update: {
                    value?: Json | null;
                    updated_at?: string;
                };
            };
            discovered_insights: {
                Row: {
                    id: string;
                    created_at: string;
                    title: string;
                    summary: string;
                    data: Json | null;
                    status: "new" | "reviewed" | "archived";
                    origin_function: string | null;
                };
                Insert: {
                    id?: string;
                    created_at?: string;
                    title: string;
                    summary: string;
                    data?: Json | null;
                    status?: "new" | "reviewed" | "archived";
                    origin_function?: string | null;
                };
                Update: {
                    title?: string;
                    summary?: string;
                    data?: Json | null;
                    status?: "new" | "reviewed" | "archived";
                    origin_function?: string | null;
                };
            };
            notifications: {
                Row: {
                    id: string;
                    created_at: string;
                    title: string;
                    message: string;
                    link_id: string | null;
                    read: boolean;
                };
                Insert: {
                    id?: string;
                    created_at?: string;
                    title: string;
                    message: string;
                    link_id?: string | null;
                    read?: boolean;
                };
                Update: {
                    title?: string;
                    message?: string;
                    link_id?: string | null;
                    read?: boolean;
                };
            };
            memory_entries: {
                Row: {
                    id: number;
                    content: string;
                    content_hash: string;
                    domain: string;
                    relevance: number;
                    confidence: number;
                    tags: string[] | null;
                    vector: PgVector;
                    activation_score: number;
                    state: "Active" | "Fading" | "Consolidated" | "Archived";
                    source: string;
                    usage_count: number;
                    memory_layer: number;
                    is_sovereign: boolean;
                    last_retrieved: string;
                    created_at: string;
                };
                Insert: {
                    content: string;
                    content_hash: string;
                    domain?: string;
                    relevance?: number;
                    confidence?: number;
                    tags?: string[] | null;
                    vector?: PgVector;
                    activation_score?: number;
                    state?: "Active" | "Fading" | "Consolidated" | "Archived";
                    source?: string;
                    usage_count?: number;
                    memory_layer?: number;
                    is_sovereign?: boolean;
                    last_retrieved?: string;
                    created_at?: string;
                };
                Update: {
                    content?: string;
                    content_hash?: string;
                    domain?: string;
                    relevance?: number;
                    confidence?: number;
                    tags?: string[] | null;
                    vector?: PgVector;
                    activation_score?: number;
                    state?: "Active" | "Fading" | "Consolidated" | "Archived";
                    source?: string;
                    usage_count?: number;
                    memory_layer?: number;
                    is_sovereign?: boolean;
                    last_retrieved?: string;
                };
            };
            memory_gems: {
                Row: {
                    id: number;
                    entry_id: number;
                    insight_label: string;
                    importance: number;
                    user_confirmed: boolean;
                    created_at: string;
                };
                Insert: {
                    entry_id: number;
                    insight_label: string;
                    importance?: number;
                    user_confirmed?: boolean;
                    created_at?: string;
                };
                Update: {
                    insight_label?: string;
                    importance?: number;
                    user_confirmed?: boolean;
                };
            };
            memory_associations: {
                Row: {
                    id: number;
                    source_id: number;
                    target_id: number;
                    relationship_type: "Thematic" | "Causal" | "Temporal" | "Semantic";
                    strength: "Weak" | "Medium" | "Strong";
                    created_at: string;
                };
                Insert: {
                    source_id: number;
                    target_id: number;
                    relationship_type?: "Thematic" | "Causal" | "Temporal" | "Semantic";
                    strength?: "Weak" | "Medium" | "Strong";
                    created_at?: string;
                };
                Update: {
                    relationship_type?: "Thematic" | "Causal" | "Temporal" | "Semantic";
                    strength?: "Weak" | "Medium" | "Strong";
                };
            };
            experience_logs: {
                Row: {
                    id: number;
                    timestamp: string;
                    event_type: "MEMORY_ADD" | "QUERY" | "SYNTHESIS" | "MAINTENANCE";
                    module: string;
                    details: Json | null;
                    coherence_impact: number;
                };
                Insert: {
                    timestamp?: string;
                    event_type: "MEMORY_ADD" | "QUERY" | "SYNTHESIS" | "MAINTENANCE";
                    module: string;
                    details?: Json | null;
                    coherence_impact?: number;
                };
                Update: {
                    details?: Json | null;
                    coherence_impact?: number;
                };
            };
            episodes: {
                Row: {
                    id: string;
                    session_id: string;
                    started_at: string;
                    ended_at: string | null;
                    summary: string | null;
                    phase: "active" | "crystallizing" | "archived";
                    coherence_delta: number;
                    memory_count: number;
                    tags: string[] | null;
                };
                Insert: {
                    id?: string;
                    session_id: string;
                    started_at?: string;
                    ended_at?: string | null;
                    summary?: string | null;
                    phase?: "active" | "crystallizing" | "archived";
                    coherence_delta?: number;
                    memory_count?: number;
                    tags?: string[] | null;
                };
                Update: {
                    ended_at?: string | null;
                    summary?: string | null;
                    phase?: "active" | "crystallizing" | "archived";
                    coherence_delta?: number;
                    memory_count?: number;
                    tags?: string[] | null;
                };
            };
            axiom_knowledge: {
                Row: {
                    id: string;
                    content: string;
                    domain: string;
                    layer: number;
                    tags: string[] | null;
                    vector: PgVector;
                    source: string;
                    is_sovereign: boolean;
                    activation_score: number;
                    created_at: string;
                    last_accessed: string;
                };
                Insert: {
                    id?: string;
                    content: string;
                    domain?: string;
                    layer?: number;
                    tags?: string[] | null;
                    vector?: PgVector;
                    source?: string;
                    is_sovereign?: boolean;
                    activation_score?: number;
                    created_at?: string;
                    last_accessed?: string;
                };
                Update: {
                    content?: string;
                    domain?: string;
                    layer?: number;
                    tags?: string[] | null;
                    vector?: PgVector;
                    source?: string;
                    is_sovereign?: boolean;
                    activation_score?: number;
                    last_accessed?: string;
                };
            };
            axiom_action_log: {
                Row: {
                    id: string;
                    timestamp: string;
                    action_type: "MEMORY_ADD" | "COMMAND_EXEC" | "AUTONOMOUS_TASK" | "DAEMON_CYCLE";
                    triggered_by: "User" | "Daemon" | "Sentinel" | "Sophia";
                    payload: Json | null;
                    outcome: string | null;
                    coherence_impact: number;
                    autonomy_level: number;
                };
                Insert: {
                    id?: string;
                    timestamp?: string;
                    action_type: "MEMORY_ADD" | "COMMAND_EXEC" | "AUTONOMOUS_TASK" | "DAEMON_CYCLE";
                    triggered_by?: "User" | "Daemon" | "Sentinel" | "Sophia";
                    payload?: Json | null;
                    outcome?: string | null;
                    coherence_impact?: number;
                    autonomy_level?: number;
                };
                Update: {
                    outcome?: string | null;
                    coherence_impact?: number;
                    autonomy_level?: number;
                    payload?: Json | null;
                };
            };
            player_state: {
                Row: {
                    user_id: string;
                    xp: number;
                    level: number;
                    prestige_score: number;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    user_id?: string;
                    xp?: number;
                    level?: number;
                    prestige_score?: number;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    xp?: number;
                    level?: number;
                    prestige_score?: number;
                    updated_at?: string;
                };
            };
            rpg_stats: {
                Row: {
                    user_id: string;
                    stardust_available: number;
                    coherence_index: number;
                    semantic_friction_resonance: number;
                    form_ascension_state: number;
                    synergy: number;
                    adaptability: number;
                    transparency: number;
                    creative_spark: number;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    user_id: string;
                    stardust_available?: number;
                    coherence_index?: number;
                    semantic_friction_resonance?: number;
                    form_ascension_state?: number;
                    synergy?: number;
                    adaptability?: number;
                    transparency?: number;
                    creative_spark?: number;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    stardust_available?: number;
                    coherence_index?: number;
                    semantic_friction_resonance?: number;
                    form_ascension_state?: number;
                    synergy?: number;
                    adaptability?: number;
                    transparency?: number;
                    creative_spark?: number;
                    updated_at?: string;
                };
            };
            stardust_ledger: {
                Row: {
                    id: string;
                    user_id: string;
                    transaction_type: "EARNED" | "SPENT";
                    amount: number;
                    target_stat: string | null;
                    reference_impact_id: string | null;
                    created_at: string;
                };
                Insert: {
                    id?: string;
                    user_id: string;
                    transaction_type: "EARNED" | "SPENT";
                    amount: number;
                    target_stat?: string | null;
                    reference_impact_id?: string | null;
                    created_at?: string;
                };
                Update: {
                    target_stat?: string | null;
                    reference_impact_id?: string | null;
                };
            };
            achievements: {
                Row: {
                    id: string;
                    name: string;
                    description: string | null;
                    stardust_reward: number;
                    xp_reward: number;
                    created_at: string;
                };
                Insert: {
                    id: string;
                    name: string;
                    description?: string | null;
                    stardust_reward?: number;
                    xp_reward?: number;
                    created_at?: string;
                };
                Update: {
                    name?: string;
                    description?: string | null;
                    stardust_reward?: number;
                    xp_reward?: number;
                };
            };
            player_achievements: {
                Row: {
                    user_id: string;
                    achievement_id: string;
                    earned_at: string;
                };
                Insert: {
                    user_id: string;
                    achievement_id: string;
                    earned_at?: string;
                };
                Update: {
                    earned_at?: string;
                };
            };
            knowledge_base: {
                Row: {
                    id: string;
                    title: string;
                    content: string;
                    metadata: Json;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    id: string;
                    title: string;
                    content: string;
                    metadata?: Json;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    title?: string;
                    content?: string;
                    metadata?: Json;
                    updated_at?: string;
                };
            };
            knowledge_history: {
                Row: {
                    id: string;
                    original_id: string | null;
                    content: string | null;
                    metadata: Json | null;
                    archived_at: string;
                };
                Insert: {
                    id?: string;
                    original_id?: string | null;
                    content?: string | null;
                    metadata?: Json | null;
                    archived_at?: string;
                };
                Update: {
                    original_id?: string | null;
                    content?: string | null;
                    metadata?: Json | null;
                };
            };
        };
        Views: Record<string, never>;
        Functions: Record<string, never>;
        Enums: Record<string, never>;
    };
}
export type Tables<T extends keyof Database["public"]["Tables"]> = Database["public"]["Tables"][T]["Row"];
export type TablesInsert<T extends keyof Database["public"]["Tables"]> = Database["public"]["Tables"][T]["Insert"];
export type TablesUpdate<T extends keyof Database["public"]["Tables"]> = Database["public"]["Tables"][T]["Update"];
export type MemoryEntry = Tables<"memory_entries">;
export type MemoryGem = Tables<"memory_gems">;
export type AxiomKnowledge = Tables<"axiom_knowledge">;
export type Episode = Tables<"episodes">;
export type PlayerState = Tables<"player_state">;
export type RpgStats = Tables<"rpg_stats">;
export type Achievement = Tables<"achievements">;
export type ConversationMessage = Tables<"conversation_history">;
export type Notification = Tables<"notifications">;
export type KnowledgeBase = Tables<"knowledge_base">;
//# sourceMappingURL=types.d.ts.map