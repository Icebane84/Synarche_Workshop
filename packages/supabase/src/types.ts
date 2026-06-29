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

// ---------------------------------------------------------------------------
// Primitive helpers
// ---------------------------------------------------------------------------

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[];

// pgvector is returned as a string from PostgREST
export type PgVector = string | null;

// ---------------------------------------------------------------------------
// Database interface
// ---------------------------------------------------------------------------

export interface Database {
  public: {
    Tables: {
      // ------------------------------------------------------------------
      // profiles — from 20251125152209_create_profiles_table
      // ------------------------------------------------------------------
      profiles: {
        Row: {
          id: string; // uuid → auth.users
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

      // ------------------------------------------------------------------
      // conversation_history — from 20251205000000_axion_schema
      // ------------------------------------------------------------------
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

      // ------------------------------------------------------------------
      // axion_state — from 20251205000000_axion_schema
      // ------------------------------------------------------------------
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

      // ------------------------------------------------------------------
      // discovered_insights — from 20251205000000_axion_schema
      // ------------------------------------------------------------------
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

      // ------------------------------------------------------------------
      // notifications — from 20251205000000_axion_schema
      // ------------------------------------------------------------------
      notifications: {
        Row: {
          id: string;
          created_at: string;
          title: string;
          message: string;
          link_id: string | null; // → discovered_insights.id
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

      // ------------------------------------------------------------------
      // memory_entries — from MEMORY-001 + content_hash migration
      // ------------------------------------------------------------------
      memory_entries: {
        Row: {
          id: number;
          content: string;
          content_hash: string;
          domain: string;
          relevance: number;
          confidence: number;
          tags: string[] | null;
          vector: PgVector; // vector(384)
          activation_score: number;
          state: "Active" | "Fading" | "Consolidated" | "Archived";
          source: string;
          usage_count: number;
          memory_layer: number; // 1=Gems, 2=Kinetic, 3=Semantic, 4=Sovereign, 5=Meta
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

      // ------------------------------------------------------------------
      // memory_gems — from MEMORY-001
      // ------------------------------------------------------------------
      memory_gems: {
        Row: {
          id: number;
          entry_id: number; // → memory_entries.id
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

      // ------------------------------------------------------------------
      // memory_associations — from MEMORY-001
      // ------------------------------------------------------------------
      memory_associations: {
        Row: {
          id: number;
          source_id: number; // → memory_entries.id
          target_id: number; // → memory_entries.id
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

      // ------------------------------------------------------------------
      // experience_logs — from MEMORY-001
      // ------------------------------------------------------------------
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

      // ------------------------------------------------------------------
      // episodes — from MEMORY-001
      // ------------------------------------------------------------------
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

      // ------------------------------------------------------------------
      // axiom_knowledge — from MEMORY-001
      // ------------------------------------------------------------------
      axiom_knowledge: {
        Row: {
          id: string;
          content: string;
          domain: string;
          layer: number; // 3=Semantic, 4=Sovereign
          tags: string[] | null;
          vector: PgVector; // vector(384)
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

      // ------------------------------------------------------------------
      // axiom_action_log — from MEMORY-001
      // ------------------------------------------------------------------
      axiom_action_log: {
        Row: {
          id: string;
          timestamp: string;
          action_type:
            | "MEMORY_ADD"
            | "COMMAND_EXEC"
            | "AUTONOMOUS_TASK"
            | "DAEMON_CYCLE";
          triggered_by: "User" | "Daemon" | "Sentinel" | "Sophia";
          payload: Json | null;
          outcome: string | null;
          coherence_impact: number;
          autonomy_level: number; // 0-5
        };
        Insert: {
          id?: string;
          timestamp?: string;
          action_type:
            | "MEMORY_ADD"
            | "COMMAND_EXEC"
            | "AUTONOMOUS_TASK"
            | "DAEMON_CYCLE";
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

      // ------------------------------------------------------------------
      // player_state — from 20260423000000_rpg_stats_schema
      // ------------------------------------------------------------------
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

      // ------------------------------------------------------------------
      // rpg_stats — from rpg_stats_schema + sync_rpg_schema_discrepancies
      // ------------------------------------------------------------------
      rpg_stats: {
        Row: {
          user_id: string; // → player_state.user_id
          stardust_available: number;
          coherence_index: number;
          semantic_friction_resonance: number;
          form_ascension_state: number;
          synergy: number;
          adaptability: number;
          transparency: number;
          creative_spark: number; // added in sync migration
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

      // ------------------------------------------------------------------
      // stardust_ledger — from 20260423000000_rpg_stats_schema
      // ------------------------------------------------------------------
      stardust_ledger: {
        Row: {
          id: string;
          user_id: string; // → player_state.user_id
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

      // ------------------------------------------------------------------
      // achievements — from 20260423000100_achievement_system
      // ------------------------------------------------------------------
      achievements: {
        Row: {
          id: string; // slug e.g. 'FIRST_GENESIS'
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

      // ------------------------------------------------------------------
      // player_achievements — from 20260423000100_achievement_system
      // ------------------------------------------------------------------
      player_achievements: {
        Row: {
          user_id: string; // → player_state.user_id
          achievement_id: string; // → achievements.id
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

      // ------------------------------------------------------------------
      // knowledge_base — from 20260526030740_create_knowledge_tables
      // ------------------------------------------------------------------
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

      // ------------------------------------------------------------------
      // knowledge_history — from 20260526030740_create_knowledge_tables
      // ------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Convenience row-type aliases
// ---------------------------------------------------------------------------

export type Tables<T extends keyof Database["public"]["Tables"]> =
  Database["public"]["Tables"][T]["Row"];

export type TablesInsert<T extends keyof Database["public"]["Tables"]> =
  Database["public"]["Tables"][T]["Insert"];

export type TablesUpdate<T extends keyof Database["public"]["Tables"]> =
  Database["public"]["Tables"][T]["Update"];

// Named row aliases for the most-used tables
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
