import { createClient } from '@supabase/supabase-js';

/**
 * The Sovereign Backend Client.
 *
 * PHASE 1: THE PERSISTENCE HANDSHAKE
 * Verified credentials from Project_Credentials.md
 */

// Fallback to hardcoded values if env vars are missing (e.g. pending restart)
const rawUrl = (import.meta.env.VITE_SUPABASE_URL as string | undefined) ?? 'https://rtjkhpotguwngfpvhfej.supabase.co';
const KEY = 
    (import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY as string | undefined) ?? 
    (import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined) ?? 
    'sb_publishable_APS-_w0TK4EeBkvmoRu5Zw_1nEsOLiD';

// Ensure URL has a protocol and no trailing slash to prevent handshake failures
const URL = (rawUrl.startsWith('http') ? rawUrl : `https://${rawUrl}`).replace(/\/$/, '');

/**
 * The sovereign Supabase client instance.
 */
export const supabase = createClient(URL, KEY);

export const isUsingPlaceholder = () => {
    return URL.includes('placeholder') || KEY.length < 50;
};
