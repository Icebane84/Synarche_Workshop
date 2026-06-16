-- Migration: Achievement System (SPEC-PROG-PERSIST-002)

-- 1. Achievement Definitions
CREATE TABLE IF NOT EXISTS achievements (
    id TEXT PRIMARY KEY, -- slug-style ID e.g. 'FIRST_GENESIS'
    name TEXT NOT NULL,
    description TEXT,
    stardust_reward INTEGER DEFAULT 0,
    xp_reward INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Player Achievement Progress (Many-to-Many)
CREATE TABLE IF NOT EXISTS player_achievements (
    user_id UUID REFERENCES player_state(user_id) ON DELETE CASCADE,
    achievement_id TEXT REFERENCES achievements(id) ON DELETE CASCADE,
    earned_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (user_id, achievement_id)
);

-- Seed Initial Achievements
INSERT INTO achievements (id, name, description, stardust_reward, xp_reward)
VALUES 
    ('FIRST_GENESIS', 'Phoenix Rebirth', 'Initiate your first Phoenix Genesis Cycle.', 500, 100),
    ('METEORITE_SURVIVOR', 'Impact Resistant', 'Successfully resolve a Meteorite Impact dissonance.', 300, 50),
    ('ARCHITECT_OF_OMEGA', 'Master Artificer', 'Reach Level 10 in all core stats.', 2000, 500)
ON CONFLICT (id) DO NOTHING;

-- Enable Realtime
alter publication supabase_realtime add table achievements;
alter publication supabase_realtime add table player_achievements;
