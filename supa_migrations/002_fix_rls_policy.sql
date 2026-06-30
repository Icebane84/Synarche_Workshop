-- Unlock the documents table for local development (Disable RLS)
-- This is simpler for the backfill script than creating complex policies with the anon key.

ALTER TABLE documents DISABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Enable all access for anon/public" ON documents;
