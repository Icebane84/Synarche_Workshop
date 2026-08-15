-- This query identifies indexes that have not been used since the last
-- statistics reset, excluding primary key constraints.
-- It's useful for finding candidates for removal to reduce storage
-- and write overhead.

SELECT
	s.schemaname,
	s.relname AS tablename,
	s.indexrelname AS indexname,
	pg_size_pretty(pg_relation_size(s.relid)) AS table_size,
	pg_size_pretty(pg_relation_size(s.indexrelid)) AS index_size
FROM
	pg_stat_user_indexes s
JOIN
	pg_index i ON s.indexrelid = i.indexrelid
WHERE
	s.idx_scan = 0      -- has never been scanned
	AND i.indisunique = false -- is not a unique constraint
	AND i.indisprimary = false -- is not a primary key
ORDER BY
	pg_relation_size(s.indexrelid) DESC;
