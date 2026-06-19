-- @conn Axion_Memory

-- Create the Axion_Memory database if it doesn't exist (MySQL dialect commented out for SQLite compatibility)
-- CREATE DATABASE IF NOT EXISTS Axion_Memory;
-- USE Axion_Memory;

-- Table for storing core memory entities
CREATE TABLE IF NOT EXISTS Memory_Nodes (
    node_id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_key TEXT NOT NULL UNIQUE,
    node_value TEXT,
    data_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_node_key ON Memory_Nodes (node_key);

-- Table for defining relationships between memory nodes
CREATE TABLE IF NOT EXISTS Memory_Relations (
    relation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_node_id INTEGER NOT NULL,
    target_node_id INTEGER NOT NULL,
    relation_type TEXT,
    weight REAL DEFAULT 1.0,
    FOREIGN KEY (source_node_id) REFERENCES Memory_Nodes(node_id) ON DELETE CASCADE,
    FOREIGN KEY (target_node_id) REFERENCES Memory_Nodes(node_id) ON DELETE CASCADE
);

-- Table for session-based context tracking
CREATE TABLE IF NOT EXISTS Session_Context (
    session_id TEXT PRIMARY KEY,
    context_blob TEXT,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
