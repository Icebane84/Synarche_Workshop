// supabaseTypes.ts
// Auto-generated types from Supabase schema
// To regenerate: npx supabase gen types typescript --project-id <your-project-id> --schema public --out-dir src/types

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json }
  | Json[];

export interface Database {
  public: {
    Tables: {
      sessions: {
        Row: {
          id: string;
          created_at: string;
          user_id: string | null;
          quest_focus: string | null;
          persona_model: string | null;
          language_preference: string | null;
          current_quest_id: string | null;
          current_persona_id: string | null;
          stats: Json;
          skills: Json;
          visual_config: Json;
          meta_cognition: Json;
          gatekeeper: Json;
          created_at: string; // Note: Supabase may return this twice, adjust if needed
        };
        Insert: {
          id?: string;
          created_at?: string;
          user_id?: string | null;
          quest_focus?: string | null;
          persona_model?: string | null;
          language_preference?: string | null;
          current_quest_id?: string | null;
          current_persona_id?: string | null;
          stats?: Json;
          skills?: Json;
          visual_config?: Json;
          meta_cognition?: Json;
          gatekeeper?: Json;
        };
        Update: {
          id?: string;
          created_at?: string;
          user_id?: string | null;
          quest_focus?: string | null;
          persona_model?: string | null;
          language_preference?: string | null;
          current_quest_id?: string | null;
          current_persona_id?: string | null;
          stats?: Json;
          skills?: Json;
          visual_config?: Json;
          meta_cognition?: Json;
          gatekeeper?: Json;
        };
      };
      quests: {
        Row: {
          id: string;
          created_at: string;
          session_id: string | null;
          title: string | null;
          status: string | null;
          objective: string | null;
          progress: number | null;
          context: string | null;
          stakes: string | null;
          constraints: Json | null;
          success_criteria: string | null;
          created_at: string; // Note: Supabase may return this twice, adjust if needed
          metadata: Json | null;
        };
        Insert: {
          id?: string;
          created_at?: string;
          session_id?: string | null;
          title?: string | null;
          status?: string | null;
          objective?: string | null;
          progress?: number | null;
          context?: string | null;
          stakes?: string | null;
          constraints?: Json | null;
          success_criteria?: string | null;
          metadata?: Json | null;
        };
        Update: {
          id?: string;
          created_at?: string;
          session_id?: string | null;
          title?: string | null;
          status?: string | null;
          objective?: string | null;
          progress?: number | null;
          context?: string | null;
          stakes?: string | null;
          constraints?: Json | null;
          success_criteria?: string | null;
          metadata?: Json | null;
        };
      };
    };
  };
}
