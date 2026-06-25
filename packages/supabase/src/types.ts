/**
 * @artifact packages/supabase/src/types.ts
 * @id        SYNC.SUPABASE.TYPES.001
 * @version   v1.0 [OMEGA]
 *
 * Supabase Database type definitions for the Synarche monorepo.
 *
 * ⚠️  THIS FILE IS AUTO-GENERATED — do not edit by hand.
 *
 * To regenerate from the live schema, run from the workspace root:
 *   npx supabase gen types typescript \
 *     --project-id rtjkhpotguwngfpvhfej \
 *     > packages/supabase/src/types.ts
 *
 * Or, if the Supabase CLI is linked locally (axion-core/supabase/):
 *   cd axion-core && npx supabase gen types typescript --local \
 *     > ../packages/supabase/src/types.ts
 */

// ---------------------------------------------------------------------------
// Placeholder — replace with generated output from `supabase gen types`
// ---------------------------------------------------------------------------

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[];

export interface Database {
  public: {
    Tables: {
      memory_entries: {
        Row: {
          id: number;
          content: string;
          domain: string | null;
          embedding: string | null; // pgvector stored as string in JS
          created_at: string;
          updated_at: string;
        };
        Insert: {
          content: string;
          domain?: string | null;
          embedding?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          content?: string;
          domain?: string | null;
          embedding?: string | null;
          updated_at?: string;
        };
      };
    };
    Views: Record<string, never>;
    Functions: Record<string, never>;
    Enums: Record<string, never>;
  };
}
