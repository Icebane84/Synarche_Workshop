/**
 * @artifact packages/supabase/src/client.ts
 * @id        SYNC.SUPABASE.CLIENT.001
 * @version   v1.1 [OMEGA]
 * @status    [ACTIVE]
 *
 * Singleton Supabase client for the Synarche monorepo.
 * Shared by axion-core, open-notebook, phoenix-rosetta-stone, nova_forge, etc.
 * Credentials sourced from NEXT_PUBLIC_SUPABASE_URL + NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY
 * defined in the workspace root .env.local — no hard-coded secrets.
 *
 * Usage (any workspace project):
 *   import { supabase } from '@synarche/supabase';
 *   const { data, error } = await supabase.from('memory_entries').select();
 */
import { type SupabaseClient } from "@supabase/supabase-js";
/**
 * Returns the shared Supabase client instance.
 * Creates it on first call; subsequent calls return the same instance.
 */
export declare function getSupabaseClient(): SupabaseClient<any>;
/** Lazy Proxy singleton export — defers client initialization until first property dereference */
export declare const supabase: SupabaseClient<any>;
//# sourceMappingURL=client.d.ts.map