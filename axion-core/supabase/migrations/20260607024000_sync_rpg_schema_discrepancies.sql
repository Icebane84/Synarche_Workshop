-- Migration: Sync RPG Schema Discrepancies (SPEC-PROG-PERSIST-003)
-- Adds missing creative_spark column to rpg_stats and aligns achievement rewards/definitions.

-- 1. Add missing creative_spark column to rpg_stats
ALTER TABLE rpg_stats 
ADD COLUMN IF NOT EXISTS creative_spark REAL DEFAULT 1.0;

-- 2. Synchronize seeded achievements with local definitions
-- Insert or update TRANSCENDENT_SYNC to match local definitions
INSERT INTO achievements (id, name, description, stardust_reward, xp_reward)
VALUES 
    ('TRANSCENDENT_SYNC', 'Transcendent Sync', 'Achieve 100% coherence across all local modules.', 1000, 500)
ON CONFLICT (id) DO UPDATE 
SET name = EXCLUDED.name,
    description = EXCLUDED.description,
    stardust_reward = EXCLUDED.stardust_reward,
    xp_reward = EXCLUDED.xp_reward;

-- Update METEORITE_SURVIVOR to align with local rewards (250 Stardust, 50 XP)
INSERT INTO achievements (id, name, description, stardust_reward, xp_reward)
VALUES 
    ('METEORITE_SURVIVOR', 'Meteorite Survivor', 'Survive the initial impact of the OMEGA migration.', 250, 50)
ON CONFLICT (id) DO UPDATE 
SET name = EXCLUDED.name,
    description = EXCLUDED.description,
    stardust_reward = EXCLUDED.stardust_reward,
    xp_reward = EXCLUDED.xp_reward;

-- Set correct names and values for other achievements if needed
INSERT INTO achievements (id, name, description, stardust_reward, xp_reward)
VALUES 
    ('FIRST_GENESIS', 'First Genesis', 'Establish your first canonical registry.', 500, 100)
ON CONFLICT (id) DO UPDATE 
SET name = EXCLUDED.name,
    description = EXCLUDED.description,
    stardust_reward = EXCLUDED.stardust_reward,
    xp_reward = EXCLUDED.xp_reward;
