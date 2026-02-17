use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::{params, Connection, Row};
use std::sync::Arc;

use super::queries_helpers::row_to_message;
use crate::p2p::message::types::*;

/// Full-text search operations using FTS5
#[derive(Clone)]
pub struct SearchQueries {
    pool: Arc<Pool<SqliteConnectionManager>>,
}

impl SearchQueries {
    /// Create new search queries handler with connection pool
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self { pool }
    }

    /// Full-text search in message content using FTS5
    pub async fn search_messages(
        &self,
        search_query: &str,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        self.search_messages_impl(search_query, limit).await
    }

    /// Implementation for message search
    async fn search_messages_impl(
        &self,
        search_query: &str,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        let pool = self.pool.clone();
        let search_query = search_query.to_string();
        let limit = limit.unwrap_or(50);

        tokio::task::spawn_blocking(move || {
            let conn = pool
                .get()
                .with_context(|| "persistence.queries_search: get conn".to_string())?;
            Self::execute_search_query(&conn, &search_query, limit)
        })
        .await
        .context("Task join error")?
    }

    /// Execute FTS search query
    fn execute_search_query(
        conn: &Connection,
        search_query: &str,
        limit: u32,
    ) -> Result<Vec<P2PMessage>> {
        let mut stmt = conn
            .prepare(
                "SELECT m.id, m.message_type, m.content, m.sender_id, m.recipient_id,
                        m.timestamp, m.signature, m.encryption_key_id, m.content_hash, m.metadata
                 FROM p2p_messages_fts fts
                 JOIN p2p_messages m ON m.id = fts.message_id
                 WHERE p2p_messages_fts MATCH ?1
                 ORDER BY rank
                 LIMIT ?2",
            )
            .with_context(|| "persistence.queries_search: prepare search query".to_string())?;

        let message_iter = stmt
            .query_map(params![search_query, limit], |row: &Row| {
                row_to_message(row)
            })
            .with_context(|| "persistence.queries_search: execute search query".to_string())?;

        let mut messages = Vec::new();
        for message_result in message_iter {
            let stored_message: StoredMessage = message_result?;
            messages.push(stored_message.message);
        }
        Ok(messages)
    }
}
