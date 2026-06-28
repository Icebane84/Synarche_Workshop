/**
 * @artifact phoenix-rosetta-stone/src/core/supabase.ts
 * Phoenix-scoped re-export of the shared @synarche/supabase client.
 * Import everything Supabase-related from here within this app.
 */

export { supabase } from "@synarche/supabase";
export type {
  Database,
  PlayerState,
  RpgStats,
  MemoryEntry,
  Achievement,
  ConversationMessage,
  Episode,
  KnowledgeBase,
  Notification,
  Json,
  Tables,
  TablesInsert,
  TablesUpdate,
} from "@synarche/supabase";
