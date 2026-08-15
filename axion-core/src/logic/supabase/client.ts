/**
 * @artifact axion-core/src/logic/supabase/client.ts
 * @id        SYNC.SUPABASE.CLIENT.AXION-PROXY
 * @version   v2.0 [OMEGA]
 *
 * Compatibility shim — re-exports the canonical client from @synarche/supabase.
 * All axion-core code importing from '@/logic/supabase' continues to work
 * without modification. Implementation now lives in packages/supabase/.
 */

/**
 * artifact_anchor:
 * - id: 
 * - type: 
 */
export { supabase, getSupabaseClient, type Database, type Json } from "@synarche/supabase";
