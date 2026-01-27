use anyhow::{Context, Result};
use rusqlite::Connection;

/// Index creation utilities for P2P message persistence schema
pub struct IndexCreator;

impl IndexCreator {
    /// Create indexes for messages table
    pub fn create_message_indexes(conn: &Connection) -> Result<()> {
        let indexes = [
            "CREATE INDEX IF NOT EXISTS idx_p2p_messages_sender ON p2p_messages(sender_id)",
            "CREATE INDEX IF NOT EXISTS idx_p2p_messages_recipient ON p2p_messages(recipient_id)",
            "CREATE INDEX IF NOT EXISTS idx_p2p_messages_timestamp ON p2p_messages(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_p2p_messages_type ON p2p_messages(message_type)",
            "CREATE INDEX IF NOT EXISTS idx_p2p_messages_hash ON p2p_messages(content_hash)",
        ];

        for index_sql in &indexes {
            conn.execute(index_sql, [])
                .with_context(|| format!("Failed to create index: {}", index_sql))?;
        }

        Ok(())
    }

    /// Create indexes for delivery status table
    pub fn create_delivery_indexes(conn: &Connection) -> Result<()> {
        let indexes = [
            "CREATE INDEX IF NOT EXISTS idx_delivery_status_message ON p2p_delivery_status(message_id)",
            "CREATE INDEX IF NOT EXISTS idx_delivery_status_peer ON p2p_delivery_status(peer_id)",
            "CREATE INDEX IF NOT EXISTS idx_delivery_status_status ON p2p_delivery_status(status)",
            "CREATE INDEX IF NOT EXISTS idx_delivery_status_retry ON p2p_delivery_status(next_retry_at)",
        ];

        for index_sql in &indexes {
            conn.execute(index_sql, [])
                .with_context(|| format!("Failed to create index: {}", index_sql))?;
        }

        Ok(())
    }

    /// Create indexes for routing history table
    pub fn create_routing_indexes(conn: &Connection) -> Result<()> {
        let indexes = [
            "CREATE INDEX IF NOT EXISTS idx_routing_history_message ON p2p_routing_history(message_id)",
            "CREATE INDEX IF NOT EXISTS idx_routing_history_peer ON p2p_routing_history(hop_peer_id)",
            "CREATE INDEX IF NOT EXISTS idx_routing_history_timestamp ON p2p_routing_history(hop_timestamp)",
        ];

        for index_sql in &indexes {
            conn.execute(index_sql, [])
                .with_context(|| format!("Failed to create index: {}", index_sql))?;
        }

        Ok(())
    }

    /// Create indexes for message events table
    pub fn create_event_indexes(conn: &Connection) -> Result<()> {
        let indexes = [
            "CREATE INDEX IF NOT EXISTS idx_message_events_message ON p2p_message_events(message_id)",
            "CREATE INDEX IF NOT EXISTS idx_message_events_type ON p2p_message_events(event_type)",
            "CREATE INDEX IF NOT EXISTS idx_message_events_processed ON p2p_message_events(processed)",
            "CREATE INDEX IF NOT EXISTS idx_message_events_timestamp ON p2p_message_events(timestamp)",
        ];

        for index_sql in &indexes {
            conn.execute(index_sql, [])
                .with_context(|| format!("Failed to create index: {}", index_sql))?;
        }

        Ok(())
    }

    /// Create all indexes in sequence
    pub fn create_all_indexes(conn: &Connection) -> Result<()> {
        Self::create_message_indexes(conn)?;
        Self::create_delivery_indexes(conn)?;
        Self::create_routing_indexes(conn)?;
        Self::create_event_indexes(conn)?;
        Ok(())
    }
}
