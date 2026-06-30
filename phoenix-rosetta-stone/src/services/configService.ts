
/**
 * @fileoverview Sovereign Configuration Service.
 * Centralizes access to environment variables and system constants,
 * adhering to the Security and Coherence mandates of the Phoenix Protocol.
 */

export const systemConfig = {
  api: {
    geminiKey: import.meta.env.GEMINI_API_KEY || import.meta.env.VITE_GEMINI_API_KEY || '',
    supabaseUrl: import.meta.env.NEXT_PUBLIC_SUPABASE_URL || import.meta.env.VITE_SUPABASE_URL || '',
    supabaseKey: import.meta.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || import.meta.env.VITE_SUPABASE_ANON_KEY || '',
  },
  constants: {
    SESSION_ID: 'SESSION-PHOENIX-001',
    IDLE_THRESHOLD_MS: 60 * 1000,
    REM_CYCLE_INTERVAL_MS: 5000,
  },
  isSimulationMode: !import.meta.env.NEXT_PUBLIC_SUPABASE_URL && !import.meta.env.VITE_SUPABASE_URL
};

export default systemConfig;
