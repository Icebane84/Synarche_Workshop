-- Migration: 005_resize_embedding_3072
-- Purpose: Resize embedding column to match Gemini-001 dimensionality (3072)
-- Created: 2026-02-08

-- 1. Drop the index first (dependencies)
DROP INDEX IF EXISTS documents_content_embedding_idx;

-- 2. Alter the column type using a casting (if data existed, but likely we can just alter)
-- Note: If data exists with 768, this might fail or pad. 
-- Since we are re-indexing, we can truncate or just alter if vector extension supports it.
-- Safer to truncate if we are re-indexing anyway, but let's try direct alter.
ALTER TABLE documents 
ALTER COLUMN embedding TYPE vector(3072);

-- 3. No Index Creation
-- Detailed Reasoning:
-- Supabase/pgvector IVFFlat indexes are capped at 2000 dimensions.
-- Our model uses 3072 dimensions.
-- For datasets < 10,000 vectors, exact search (Scanning) is extremely fast and accurate.
-- We will proceed WITHOUT an index.
-- CREATE INDEX ... (OMITTED)
