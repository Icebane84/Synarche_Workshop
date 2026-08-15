/**
 * The Sovereign Backend Client.
 * Re-exports the unified @synarche/supabase client.
 */

export const isUsingPlaceholder = () => {
    // @ts-ignore
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL || import.meta.env.VITE_SUPABASE_URL || '';
    // @ts-ignore
    const key = process.env.SUPABASE_ANON_KEY || import.meta.env.VITE_SUPABASE_ANON_KEY || '';
    return !url || url.includes('placeholder') || key.length < 20;
};


export { supabase } from '@synarche/supabase';
