-- Create the Axion_Memory database if it doesn't exist
CREATE DATABASE IF NOT EXISTS Axion_Memory;
USE Axion_Memory;

-- Table for storing core memory entities
CREATE TABLE IF NOT EXISTS Memory_Nodes (
    node_id INT AUTO_INCREMENT PRIMARY KEY,
    node_key VARCHAR(255) NOT NULL UNIQUE,
    node_value TEXT,
    data_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_node_key (node_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table for defining relationships between memory nodes
CREATE TABLE IF NOT EXISTS Memory_Relations (
    relation_id INT AUTO_INCREMENT PRIMARY KEY,
    source_node_id INT NOT NULL,
    target_node_id INT NOT NULL,
    relation_type VARCHAR(100),
    weight FLOAT DEFAULT 1.0,
    FOREIGN KEY (source_node_id) REFERENCES Memory_Nodes(node_id) ON DELETE CASCADE,
    FOREIGN KEY (target_node_id) REFERENCES Memory_Nodes(node_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table for session-based context tracking
CREATE TABLE IF NOT EXISTS Session_Context (
    session_id VARCHAR(255) PRIMARY KEY,
    context_blob JSON,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
