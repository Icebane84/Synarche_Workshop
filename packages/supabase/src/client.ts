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

import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "./types.js";

// ---------------------------------------------------------------------------
// Env resolution
// Supports both Node (process.env) and browser (import.meta.env) runtimes.
// ---------------------------------------------------------------------------

function resolveEnv(key: string): string | undefined {
  // Node / VS Code extension / scripts
  if (typeof process !== "undefined" && process.env) {
    const val = process.env[key];
    if (val) return val;
  }
  // Vite / browser (phoenix-rosetta-stone, open-notebook frontend)
  // @ts-ignore — import.meta.env is injected by Vite at build time
  if (typeof import.meta !== "undefined" && (import.meta as any).env) {
    // @ts-ignore
    return (import.meta as any).env[key];
  }
  return undefined;
}

const supabaseUrl = resolveEnv("NEXT_PUBLIC_SUPABASE_URL");
const supabaseKey =
  resolveEnv("SUPABASE_ANON_KEY") ??
  resolveEnv("NEXT_PUBLIC_SUPABASE_ANON_KEY") ??
  resolveEnv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY") ??
  resolveEnv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY");

console.log("[Synarche · Supabase] Initializing client with:", {
  url: supabaseUrl,
  hasKey: !!supabaseKey,
  keySnippet: supabaseKey ? `${supabaseKey.substring(0, 8)}...` : undefined,
  resolvedFrom: supabaseKey === resolveEnv("SUPABASE_ANON_KEY") ? "SUPABASE_ANON_KEY" : "PUBLISHABLE_KEY"
});

if (!supabaseUrl) {
  throw new Error(
    "[Synarche · Supabase] NEXT_PUBLIC_SUPABASE_URL is not defined. " +
      "Check .env.local at the workspace root.",
  );
}

if (!supabaseKey) {
  throw new Error(
    "[Synarche · Supabase] No Supabase key found. " +
      "Set NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY or SUPABASE_ANON_KEY in .env.local.",
  );
}

// ---------------------------------------------------------------------------
// Singleton client
// Lazily initialised — safe for both extension (Node) and browser contexts.
// ---------------------------------------------------------------------------

let _client: SupabaseClient<Database> | null = null;

/**
 * Returns the shared Supabase client instance.
 * Creates it on first call; subsequent calls return the same instance.
 */
export function getSupabaseClient(): SupabaseClient<Database> {
  if (!_client) {
    const isNode =
      typeof process !== "undefined" &&
      typeof (process as any).versions?.node !== "undefined";

    _client = createClient<Database>(supabaseUrl!, supabaseKey!, {
      auth: {
        // Disable browser-only auth storage when running in Node/VS Code
        persistSession: !isNode,
        autoRefreshToken: !isNode,
        detectSessionInUrl: !isNode,
      },
    });
  }
  return _client;
}

/** Convenience singleton export */
export const supabase = getSupabaseClient();
