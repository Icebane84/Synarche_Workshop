/** @nexus GVRN.Core.Nexus.Backend */

import { createClient } from '@supabase/supabase-js';

// Environment variables must be set in .env.local
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://rtjkhpotguwngfpvhfej.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'sb_publishable_APS-_w0TK4EeBkvmoRu5Zw_1nEsOLiD';

/**
 * The Sovereign Backend Connector
 * Provides direct access to the Supabase Postgres DB and Edge Functions.
 */
export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// --- 1. INSERT NEW TOOL: STRATEGIST KIT ---

// Insert the Strategist tool into the tools table
export const addTool = async () => {
    const { data, error } = await supabase
        .from('tools')
        .insert([
            {
                name: 'Strategist',
                description: 'Provides strategic guidance and planning',
                category: 'Strategic',
                defaultEnabled: true,
            },
        ])
        .select()
        .single();

    if (error) {
        console.error('Error adding tool:', error);
        return {
            success: false,
            error,
        };
    }

    console.log('Tool added successfully:', data);
    return {
        success: true,
        data,
    };
};

// --- 2. DEFINE THE TOOL OBJECTS ---

export const strategist = {
    name: 'Strategist',
    description: 'Provides strategic guidance and planning',
    category: 'Strategic',
    defaultEnabled: true,
} as const;

export const tools = {
    strategist,
};
