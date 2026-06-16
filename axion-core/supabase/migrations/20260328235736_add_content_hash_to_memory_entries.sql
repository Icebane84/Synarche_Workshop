
-- Add content_hash column for performant deduplication
ALTER TABLE memory_entries ADD COLUMN IF NOT EXISTS content_hash TEXT UNIQUE;

-- Backfill content_hash for existing entries if any
UPDATE memory_entries SET content_hash = encode(sha256(content::bytea), 'hex') WHERE content_hash IS NULL;

-- Ensure it's not null for future inserts
ALTER TABLE memory_entries ALTER COLUMN content_hash SET NOT NULL;
;
