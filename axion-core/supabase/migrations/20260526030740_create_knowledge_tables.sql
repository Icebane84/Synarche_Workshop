CREATE TABLE IF NOT EXISTS knowledge_base (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS knowledge_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_id TEXT,
    content TEXT,
    metadata JSONB,
    archived_at TIMESTAMPTZ DEFAULT now()
);;
