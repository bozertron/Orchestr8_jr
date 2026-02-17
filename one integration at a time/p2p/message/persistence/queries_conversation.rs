#[path = "queries_conversation_helpers.rs"]
mod queries_conversation_helpers;

use anyhow::{Context, Result};
use libp2p::PeerId;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::params;
use std::sync::Arc;

use super::queries_helpers::row_to_message;
use crate::p2p::message::types::*;
use queries_conversation_helpers::{build_recent_conversations_query, parse_conversation_row};

/// Conversation-based message queries (Task 3.5 Priority 1)
#[derive(Clone)]
pub struct ConversationQueries {
    pool: Arc<Pool<SqliteConnectionManager>>,
}

impl ConversationQueries {
    /// Create new conversation queries handler
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self { pool }
    }

    /// Get messages for a conversation (bidirectional between two peers)
    pub async fn get_conversation_messages(
        &self,
        peer_id: &PeerId,
        limit: Option<u32>,
        offset: Option<u32>,
    ) -> Result<Vec<StoredMessage>> {
        let pool = self.pool.clone();
        let peer_id_str = peer_id.to_string();
        let limit = limit.unwrap_or(100);
        let offset = offset.unwrap_or(0);

        tokio::task::spawn_blocking(move || {
            Self::query_conversation(&pool, &peer_id_str, limit, offset)
        })
        .await
        .context("Task join error")?
    }

    /// Query conversation messages from database
    fn query_conversation(
        pool: &Pool<SqliteConnectionManager>,
        peer_id: &str,
        limit: u32,
        offset: u32,
    ) -> Result<Vec<StoredMessage>> {
        let conn = pool.get().context("Failed to get database connection")?;

        let mut stmt = conn.prepare(
            "SELECT id, message_type, content, sender_id, recipient_id,
                    timestamp, signature, encryption_key_id, content_hash, metadata
             FROM p2p_messages
             WHERE (sender_id = ?1 OR recipient_id = ?1)
             ORDER BY timestamp DESC
             LIMIT ?2 OFFSET ?3",
        )?;

        let messages = stmt
            .query_map(params![peer_id, limit, offset], |row| row_to_message(row))?
            .collect::<rusqlite::Result<Vec<_>>>()?;

        Ok(messages)
    }

    /// Get conversation message count
    pub async fn get_conversation_count(&self, peer_id: &PeerId) -> Result<u32> {
        let pool = self.pool.clone();
        let peer_id_str = peer_id.to_string();

        tokio::task::spawn_blocking(move || Self::query_conversation_count(&pool, &peer_id_str))
            .await
            .context("Task join error")?
    }

    /// Query conversation message count
    fn query_conversation_count(
        pool: &Pool<SqliteConnectionManager>,
        peer_id: &str,
    ) -> Result<u32> {
        let conn = pool.get().context("Failed to get database connection")?;

        let count: u32 = conn.query_row(
            "SELECT COUNT(*) FROM p2p_messages
             WHERE (sender_id = ?1 OR recipient_id = ?1)",
            params![peer_id],
            |row| row.get(0),
        )?;

        Ok(count)
    }

    /// Get recent conversations (list of peers with last message)
    pub async fn get_recent_conversations(
        &self,
        limit: Option<u32>,
    ) -> Result<Vec<(PeerId, StoredMessage)>> {
        let pool = self.pool.clone();
        let limit = limit.unwrap_or(20);

        tokio::task::spawn_blocking(move || Self::query_recent_conversations(&pool, limit))
            .await
            .context("Task join error")?
    }

    /// Query recent conversations
    fn query_recent_conversations(
        pool: &Pool<SqliteConnectionManager>,
        limit: u32,
    ) -> Result<Vec<(PeerId, StoredMessage)>> {
        let conn = pool.get().context("Failed to get database connection")?;

        let mut stmt = conn.prepare(build_recent_conversations_query())?;

        let results = stmt
            .query_map(params![limit], parse_conversation_row)?
            .collect::<rusqlite::Result<Vec<_>>>()?;

        Ok(results)
    }

    /// Get unread message count for conversation
    pub async fn get_unread_count(&self, peer_id: &PeerId) -> Result<u32> {
        let pool = self.pool.clone();
        let peer_id_str = peer_id.to_string();

        tokio::task::spawn_blocking(move || Self::query_unread_count(&pool, &peer_id_str))
            .await
            .context("Task join error")?
    }

    /// Query unread message count
    fn query_unread_count(pool: &Pool<SqliteConnectionManager>, peer_id: &str) -> Result<u32> {
        let conn = pool.get().context("Failed to get database connection")?;

        // Count messages where sender is the peer and status is not 'read'
        let count: u32 = conn.query_row(
            "SELECT COUNT(*) FROM p2p_messages m
             JOIN p2p_delivery_status d ON m.id = d.message_id
             WHERE m.sender_id = ?1
             AND d.status NOT IN ('delivered', 'read')",
            params![peer_id],
            |row| row.get(0),
        )?;

        Ok(count)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_conversation_queries_creation() {
        let manager = SqliteConnectionManager::memory();
        let pool = Pool::new(manager).unwrap();
        let queries = ConversationQueries::new(Arc::new(pool));
        // Queries created successfully
    }
}
