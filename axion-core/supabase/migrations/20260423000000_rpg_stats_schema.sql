-- Migration: RPG Stats Schema (SPEC-PROG-PERSIST-001)

-- 1. Player State (Core XP and Prestige Tracking)
CREATE TABLE IF NOT EXISTS player_state (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    prestige_score INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 2. RPG Stats (The Celestial Chart Metrics)
CREATE TABLE IF NOT EXISTS rpg_stats (
    user_id UUID PRIMARY KEY REFERENCES player_state(user_id) ON DELETE CASCADE,
    stardust_available INTEGER DEFAULT 0,
    coherence_index REAL DEFAULT 1.0,
    semantic_friction_resonance REAL DEFAULT 1.0,
    form_ascension_state REAL DEFAULT 1.0,
    synergy REAL DEFAULT 1.0,
    adaptability REAL DEFAULT 1.0,
    transparency REAL DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Stardust Transaction Ledger (Audit Trail)
CREATE TABLE IF NOT EXISTS stardust_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES player_state(user_id) ON DELETE CASCADE,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('EARNED', 'SPENT')),
    amount INTEGER NOT NULL,
    target_stat TEXT,
    reference_impact_id TEXT, -- Ties back to a Meteorite Impact
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Enable Realtime for Player State and RPG Stats
alter publication supabase_realtime add table player_state;
alter publication supabase_realtime add table rpg_stats;
