use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::{params, Connection, OptionalExtension, Row};
use std::sync::Arc;

use super::queries_helpers::{row_to_message, MessageFilter};
use crate::p2p::message::types::*;

/// Basic message retrieval operations
#[derive(Clone)]
pub struct BasicQueries {
    pool: Arc<Pool<SqliteConnectionManager>>,
}

impl BasicQueries {
    /// Create new basic queries handler with connection pool
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self { pool }
    }

    /// Get message by ID with full details
    pub async fn get_message_by_id(&self, message_id: &MessageId) -> Result<Option<StoredMessage>> {
        let pool = self.pool.clone();
        let id = message_id.clone();
        tokio::task::spawn_blocking(move || Self::query_message_by_id(pool, id))
            .await
            .context("Task join error")?
    }

    fn query_message_by_id(
        pool: Arc<Pool<SqliteConnectionManager>>,
        message_id: MessageId,
    ) -> Result<Option<StoredMessage>> {
        let conn = pool
            .get()
            .with_context(|| "persistence.queries_basic: get conn".to_string())?;

        let mut stmt = conn
            .prepare(
                "SELECT id, message_type, content, sender_id, recipient_id,
                        timestamp, signature, encryption_key_id, content_hash, metadata
                 FROM p2p_messages WHERE id = ?1",
            )
            .with_context(|| "persistence.queries_basic: prepare get_message_by_id".to_string())?;

        let message_opt = stmt
            .query_row(params![message_id.to_string()], |row: &Row| {
                row_to_message(row)
            })
            .optional()
            .with_context(|| {
                format!(
                    "persistence.queries_basic: get_message_by_id id={}",
                    message_id
                )
            })?;

        Ok(message_opt)
    }

    /// Get messages with filtering and pagination
    pub async fn get_messages_filtered(&self, filter: &MessageFilter) -> Result<Vec<P2PMessage>> {
        let stored_messages = self.get_messages_filtered_impl(filter).await?;
        Ok(stored_messages.into_iter().map(|sm| sm.message).collect())
    }

    /// Implementation for filtered message retrieval
    async fn get_messages_filtered_impl(
        &self,
        filter: &MessageFilter,
    ) -> Result<Vec<StoredMessage>> {
        let pool = self.pool.clone();
        let filter = filter.clone();

        tokio::task::spawn_blocking(move || {
            let conn = pool.get().context("Failed to get database connection")?;
            Self::execute_filtered_query(&conn, &filter)
        })
        .await
        .context("Task join error")?
    }

    /// Execute filtered query and collect results
    fn execute_filtered_query(
        conn: &Connection,
        filter: &MessageFilter,
    ) -> Result<Vec<StoredMessage>> {
        let (query, params) = Self::build_filtered_query(filter);
        let mut stmt = conn
            .prepare(&query)
            .with_context(|| format!("persistence.queries_basic: prepare filtered query"))?;
        let message_iter = stmt
            .query_map(rusqlite::params_from_iter(params.iter()), |row: &Row| {
                row_to_message(row)
            })
            .with_context(|| format!("persistence.queries_basic: execute filtered query"))?;

        let mut messages = Vec::new();
        for message_result in message_iter {
            messages.push(message_result?);
        }
        Ok(messages)
    }

    /// Build filtered query with dynamic WHERE conditions
    fn build_filtered_query(filter: &MessageFilter) -> (String, Vec<String>) {
        let mut query = Self::build_base_query();
        let mut params = Vec::new();

        Self::add_filter_conditions(&mut query, &mut params, filter);
        Self::add_ordering_and_pagination(&mut query, &mut params, filter);

        (query, params)
    }

    /// Build base SELECT query
    fn build_base_query() -> String {
        String::from(
            "SELECT id, message_type, content, sender_id, recipient_id,
                    timestamp, signature, encryption_key_id, content_hash, metadata
             FROM p2p_messages WHERE 1=1",
        )
    }

    /// Add WHERE conditions to query
    fn add_filter_conditions(query: &mut String, params: &mut Vec<String>, filter: &MessageFilter) {
        if let Some(sender_id) = &filter.sender_id {
            query.push_str(" AND sender_id = ?");
            params.push(sender_id.to_string());
        }
        if let Some(recipient_id) = &filter.recipient_id {
            query.push_str(" AND recipient_id = ?");
            params.push(recipient_id.to_string());
        }
        if let Some(message_type) = &filter.message_type {
            query.push_str(" AND message_type = ?");
            params.push(message_type.clone());
        }
        if let Some(start_timestamp) = filter.start_timestamp {
            query.push_str(" AND timestamp >= ?");
            params.push(start_timestamp.to_string());
        }
        if let Some(end_timestamp) = filter.end_timestamp {
            query.push_str(" AND timestamp <= ?");
            params.push(end_timestamp.to_string());
        }
    }

    /// Add ordering and pagination to query
    fn add_ordering_and_pagination(
        query: &mut String,
        params: &mut Vec<String>,
        filter: &MessageFilter,
    ) {
        query.push_str(" ORDER BY timestamp DESC");
        if let Some(limit) = filter.limit {
            query.push_str(" LIMIT ?");
            params.push(limit.to_string());
        }
        if let Some(offset) = filter.offset {
            query.push_str(" OFFSET ?");
            params.push(offset.to_string());
        }
    }
}
