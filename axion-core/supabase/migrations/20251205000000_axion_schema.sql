-- Migration: Axion Schema (SPEC-SUPABASE-001)

-- 1. Conversation History
CREATE TABLE IF NOT EXISTS conversation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    sender TEXT NOT NULL CHECK (sender IN ('Chris', 'Axion')),
    content TEXT NOT NULL,
    session_id UUID NOT NULL,
    metadata JSONB DEFAULT '{}'
);

-- 2. Axion State
CREATE TABLE IF NOT EXISTS axion_state (
    key TEXT PRIMARY KEY,
    value JSONB,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Discovered Insights
CREATE TABLE IF NOT EXISTS discovered_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    data JSONB,
    status TEXT DEFAULT 'new' CHECK (status IN ('new', 'reviewed', 'archived')),
    origin_function TEXT
);

-- 4. Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    link_id UUID REFERENCES discovered_insights(id),
    read BOOLEAN DEFAULT FALSE
);

-- Enable Realtime for Chat and Notifications
alter publication supabase_realtime add table conversation_history;
alter publication supabase_realtime add table notifications;
