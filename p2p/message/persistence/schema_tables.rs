use anyhow::{Context, Result};
use rusqlite::Connection;

/// Table creation utilities for P2P message persistence schema
pub struct TableCreator;

impl TableCreator {
    /// Create main messages table
    pub fn create_messages_table(conn: &Connection) -> Result<()> {
        conn.execute(
            "CREATE TABLE IF NOT EXISTS p2p_messages (
                id TEXT PRIMARY KEY,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                sender_id TEXT NOT NULL,
                recipient_id TEXT,
                timestamp INTEGER NOT NULL,
                signature BLOB,
                encryption_key_id TEXT,
                content_hash TEXT NOT NULL,
                metadata TEXT,
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                updated_at INTEGER NOT NULL DEFAULT (unixepoch())
            )",
            [],
        )
        .context("Failed to create p2p_messages table")?;
        Ok(())
    }

    /// Create delivery status table
    pub fn create_delivery_status_table(conn: &Connection) -> Result<()> {
        conn.execute(
            "CREATE TABLE IF NOT EXISTS p2p_delivery_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT NOT NULL,
                peer_id TEXT NOT NULL,
                status TEXT NOT NULL,
                transport_method TEXT NOT NULL,
                attempt_count INTEGER NOT NULL DEFAULT 0,
                last_attempt_at INTEGER,
                next_retry_at INTEGER,
                error_message TEXT,
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
                FOREIGN KEY (message_id) REFERENCES p2p_messages(id) ON DELETE CASCADE
            )",
            [],
        )
        .context("Failed to create p2p_delivery_status table")?;
        Ok(())
    }

    /// Create routing history table
    pub fn create_routing_history_table(conn: &Connection) -> Result<()> {
        conn.execute(
            "CREATE TABLE IF NOT EXISTS p2p_routing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT NOT NULL,
                hop_peer_id TEXT NOT NULL,
                transport_method TEXT NOT NULL,
                hop_timestamp INTEGER NOT NULL,
                latency_ms INTEGER,
                success BOOLEAN NOT NULL,
                error_details TEXT,
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                FOREIGN KEY (message_id) REFERENCES p2p_messages(id) ON DELETE CASCADE
            )",
            [],
        )
        .context("Failed to create p2p_routing_history table")?;
        Ok(())
    }

    /// Create message events table
    pub fn create_message_events_table(conn: &Connection) -> Result<()> {
        conn.execute(
            "CREATE TABLE IF NOT EXISTS p2p_message_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT,
                peer_id TEXT,
                timestamp INTEGER NOT NULL,
                processed BOOLEAN NOT NULL DEFAULT FALSE,
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                FOREIGN KEY (message_id) REFERENCES p2p_messages(id) ON DELETE CASCADE
            )",
            [],
        )
        .context("Failed to create p2p_message_events table")?;
        Ok(())
    }

    /// Create all tables in sequence
    pub fn create_all_tables(conn: &Connection) -> Result<()> {
        Self::create_messages_table(conn)?;
        Self::create_delivery_status_table(conn)?;
        Self::create_routing_history_table(conn)?;
        Self::create_message_events_table(conn)?;
        Ok(())
    }
}
