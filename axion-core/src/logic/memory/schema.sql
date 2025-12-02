-- ID: CORE-LOGIC-MEM-SCHEMA-001
-- Status: [CANONIZED]
-- Genesis Stamp: 2026-03-07
-- Domain: LOGIC.MEMORY
-- Evolution: OMEGA Ascension

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Table for active memory entries
CREATE TABLE IF NOT EXISTS memory_entries (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    domain TEXT DEFAULT 'GeneralKnowledge',
    relevance REAL DEFAULT 0.5,
    confidence REAL DEFAULT 1.0,
    tags TEXT[],
    vector vector(1536), -- Storing embedding as native vector
    activation_score REAL DEFAULT 0.5,
    state TEXT DEFAULT 'Active',
    source TEXT DEFAULT 'Unknown',
    usage_count INTEGER DEFAULT 0,
    memory_layer INTEGER DEFAULT 2, -- L1-L5
    is_sovereign BOOLEAN DEFAULT FALSE, -- L4 status
    last_retrieved TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for high-priority validated insights (L1 Gems)
CREATE TABLE IF NOT EXISTS memory_gems (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER REFERENCES memory_entries(id) ON DELETE CASCADE,
    insight_label TEXT NOT NULL,
    importance REAL DEFAULT 1.0,
    user_confirmed BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for semantic associations (Soft Links)
CREATE TABLE IF NOT EXISTS memory_associations (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES memory_entries(id) ON DELETE CASCADE,
    target_id INTEGER REFERENCES memory_entries(id) ON DELETE CASCADE,
    relationship_type TEXT DEFAULT 'Thematic',
    strength TEXT DEFAULT 'Weak',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_id, target_id)
);

-- Table for detailed experience logs
CREATE TABLE IF NOT EXISTS experience_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT NOT NULL,
    module TEXT NOT NULL,
    details JSONB,
    coherence_impact REAL DEFAULT 0.0
);

-- Indexing for fuzzy search and retrieval performance
CREATE INDEX IF NOT EXISTS idx_memory_content ON memory_entries USING gin(to_tsvector('english', content));
CREATE INDEX IF NOT EXISTS idx_memory_activation ON memory_entries (activation_score DESC);
CREATE INDEX IF NOT EXISTS idx_memory_state ON memory_entries (state);
CREATE INDEX IF NOT EXISTS idx_memory_domain ON memory_entries (domain);
CREATE INDEX IF NOT EXISTS idx_experience_module ON experience_logs (module);
CREATE INDEX IF NOT EXISTS idx_experience_timestamp ON experience_logs (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_assoc_source ON memory_associations (source_id);
CREATE INDEX IF NOT EXISTS idx_assoc_target ON memory_associations (target_id);
