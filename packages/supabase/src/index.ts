/**
 * @artifact packages/supabase/src/index.ts
 * Public API for @synarche/supabase
 */

export { supabase, getSupabaseClient } from "./client.js";
export type {
  Database,
  Json,
  PgVector,
  Tables,
  TablesInsert,
  TablesUpdate,
  // Named row aliases
  MemoryEntry,
  MemoryGem,
  AxiomKnowledge,
  Episode,
  PlayerState,
  RpgStats,
  Achievement,
  ConversationMessage,
  Notification,
  KnowledgeBase,
} from "./types.js";
