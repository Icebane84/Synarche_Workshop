-- ========================================================
-- PHOENIX SYNARCHE: 1-CLICK SUPABASE TABLE UNLOCK & SEED SQL (v15.1)
-- Paste this script into your Supabase Dashboard -> SQL Editor
-- ========================================================

-- 1. Enable pgvector extension for RAG Search
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Unlock RLS Policies for Development
ALTER TABLE IF EXISTS memory_entries DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS knowledge_base DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS documents DISABLE ROW LEVEL SECURITY;

-- 3. Ensure Table Schemas Exist with Default Hash Handling
CREATE TABLE IF NOT EXISTS memory_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    content_hash TEXT DEFAULT md5(random()::text),
    domain VARCHAR(64) DEFAULT 'General',
    memory_layer INTEGER DEFAULT 2,
    tags TEXT[] DEFAULT '{}',
    activation_score FLOAT DEFAULT 0.85,
    state VARCHAR(32) DEFAULT 'Active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- If content_hash column exists but lacks a default, set a default generator
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'memory_entries' AND column_name = 'content_hash'
    ) THEN
        ALTER TABLE memory_entries ALTER COLUMN content_hash SET DEFAULT md5(random()::text);
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS knowledge_base (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(3072),
    metadata JSONB DEFAULT '{}'
);

-- 4. Seed Primary Records into knowledge_base
INSERT INTO knowledge_base (id, title, content, metadata) VALUES
('PHOENIX_PROTOCOL_BLUEPRINT', 'The Phoenix Protocol (Architecture)', 'The Phoenix Protocol defines the component-driven cognitive architecture of the Rosetta Stone system.', '{"category": "Protocol", "tags": ["protocol", "architecture"]}'),
('PHOENIX_CODEX_V15_1', 'The Phoenix Codex (43-Law Codex v15.1)', 'Law 01: Struggle. Law 02: Naming. Law 03: Failure as Fuel. Law 04: Cognitive Loom. Law 11: NIM Detection.', '{"category": "Codex", "tags": ["codex", "governance"]}'),
('UMB_LEX_001', 'UMB-LEX-001: The Master Lexicon & Rosetta Stone Concordance', 'Master concordance mapping Phoenix Rosetta Stone (PRS-001), Dissonance Quests, Actionable Prompt Packets, and NIM.', '{"category": "Protocol", "tags": ["lexicon", "concordance"]}'),
('WHERE_LIGHT_FADES_ASHEN_OATH', 'Where Light Fades: Ashen Oath Master Lore Substrate', 'Master lore substrate detailing Kaelen, Serafina, Eldrin, Brother Malakor, Silent Spire, and the Architecture of Flesh.', '{"category": "Codex", "tags": ["ashen-oath", "where-light-fades", "lore"]}'),
('DYNAMIC_ROSETTA_BLUEPRINT', 'Blueprint for Dynamic Rosetta Stone App', 'Master technical blueprint for Component-Driven Cognition, Supabase Sovereign Backend, React 19, and D3.js physics.', '{"category": "Blueprint", "tags": ["blueprint", "rosetta-stone"]}')
ON CONFLICT (id) DO UPDATE SET content = EXCLUDED.content, title = EXCLUDED.title;

-- 5. Seed Memory Graph Nodes into memory_entries with Computed content_hash
INSERT INTO memory_entries (content, content_hash, domain, memory_layer, tags, activation_score) VALUES
('Kaelen: Volatile Vanguard wielder of Oathbringer', md5('Kaelen: Volatile Vanguard wielder of Oathbringer'), 'Character', 2, ARRAY['character', 'protagonist'], 0.95),
('Serafina: Warden projecting Consecrated Circle of White Flame', md5('Serafina: Warden projecting Consecrated Circle of White Flame'), 'Character', 2, ARRAY['character', 'warden'], 0.90),
('Eldrin: Prisoner turned ally transmuting arcana in Act 2', md5('Eldrin: Prisoner turned ally transmuting arcana in Act 2'), 'Character', 2, ARRAY['character', 'mage'], 0.85),
('Brother Malakor: Antagonist orchestrating Architecture of Flesh', md5('Brother Malakor: Antagonist orchestrating Architecture of Flesh'), 'Character', 2, ARRAY['character', 'antagonist'], 0.90),
('Valerius: Architect of Chains commanding the Silent Spire', md5('Valerius: Architect of Chains commanding the Silent Spire'), 'Character', 2, ARRAY['character', 'architect'], 0.88),
('Silent Spire: Tower sanctuary and trial chamber of the Ashen Order', md5('Silent Spire: Tower sanctuary and trial chamber of the Ashen Order'), 'Location', 2, ARRAY['location', 'sanctuary'], 0.80),
('The Stain: Spectral corruption infesting the inner world', md5('The Stain: Spectral corruption infesting the inner world'), 'Location', 2, ARRAY['location', 'hazard'], 0.85);

-- 6. Seed Initial RAG Documents into documents
INSERT INTO documents (content, metadata) VALUES
('# The Phoenix Protocol (Architecture)\nCategory: Protocol\n\nThe Phoenix Protocol defines the component-driven cognitive architecture of the Rosetta Stone system.', '{"docId": "PHOENIX_PROTOCOL_BLUEPRINT", "title": "The Phoenix Protocol (Architecture)", "type": "Protocol"}'),
('# The Phoenix Codex (43-Law Codex v15.1)\nCategory: Codex\n\nLaw 01: Struggle. Law 02: Naming. Law 03: Failure as Fuel. Law 04: Cognitive Loom. Law 11: NIM Detection.', '{"docId": "PHOENIX_CODEX_V15_1", "title": "The Phoenix Codex (43-Law Codex v15.1)", "type": "Codex"}'),
('# UMB-LEX-001: The Master Lexicon & Rosetta Stone Concordance\nCategory: Protocol\n\nMaster concordance mapping Phoenix Rosetta Stone (PRS-001), Dissonance Quests, Actionable Prompt Packets, and NIM.', '{"docId": "UMB_LEX_001", "title": "UMB-LEX-001: The Master Lexicon & Rosetta Stone Concordance", "type": "Protocol"}'),
('# Where Light Fades: Ashen Oath Master Lore Substrate\nCategory: Codex\n\nMaster lore substrate detailing Kaelen, Serafina, Eldrin, Brother Malakor, Silent Spire, and the Architecture of Flesh.', '{"docId": "WHERE_LIGHT_FADES_ASHEN_OATH", "title": "Where Light Fades: Ashen Oath Master Lore Substrate", "type": "Codex"}'),
('# Blueprint for Dynamic Rosetta Stone App\nCategory: Blueprint\n\nMaster technical blueprint for Component-Driven Cognition, Supabase Sovereign Backend, React 19, and D3.js physics.', '{"docId": "DYNAMIC_ROSETTA_BLUEPRINT", "title": "Blueprint for Dynamic Rosetta Stone App", "type": "Blueprint"}');

-- 7. Create match_documents Vector Search RPC Function
CREATE OR REPLACE FUNCTION match_documents (
    query_embedding VECTOR(3072),
    match_threshold FLOAT,
    match_count INT
)
RETURNS TABLE (
    id BIGINT,
    content TEXT,
    similarity FLOAT,
    metadata JSONB
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.content,
        1 - (d.embedding <=> query_embedding) AS similarity,
        d.metadata
    FROM documents d
    WHERE d.embedding IS NOT NULL AND 1 - (d.embedding <=> query_embedding) > match_threshold
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
