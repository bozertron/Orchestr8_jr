use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;
use tokio::sync::mpsc;
use tracing::info;

use crate::p2p::message::types::MessageId;
use crate::p2p::MessageEvent;
use rusqlite::Connection;
use std::str::FromStr;

/// Database cleanup operations for message events
#[derive(Clone)]
pub struct ProcessorCleanup {
    pool: Arc<Pool<SqliteConnectionManager>>,
    event_sender: Option<mpsc::UnboundedSender<MessageEvent>>,
}

impl ProcessorCleanup {
    /// Create new cleanup processor
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self {
            pool,
            event_sender: None,
        }
    }

    /// Optional event sender injection (builder)
    pub fn with_event_sender(mut self, sender: mpsc::UnboundedSender<MessageEvent>) -> Self {
        self.event_sender = Some(sender);
        self
    }

    /// Clean up old processed events
    pub async fn cleanup_old_events(&self, older_than_days: u32) -> Result<u32> {
        let pool = self.pool.clone();
        let cutoff_timestamp = self.calculate_cutoff_timestamp(older_than_days);
        let sender = self.event_sender.clone();

        let result = tokio::task::spawn_blocking(move || {
            Self::execute_cleanup_query(pool, cutoff_timestamp, sender)
        })
        .await
        .with_context(|| "persistence.processor_cleanup: join cleanup task".to_string())?;

        result
    }

    /// Calculate cutoff timestamp for cleanup
    fn calculate_cutoff_timestamp(&self, older_than_days: u32) -> i64 {
        chrono::Utc::now().timestamp() - (older_than_days as i64 * 24 * 60 * 60)
    }

    /// Execute cleanup query
    fn execute_cleanup_query(
        pool: Arc<Pool<SqliteConnectionManager>>,
        cutoff_timestamp: i64,
        event_sender: Option<mpsc::UnboundedSender<MessageEvent>>,
    ) -> Result<u32> {
        let conn = pool
            .get()
            .with_context(|| "persistence.processor_cleanup: get conn".to_string())?;

        let message_ids = fetch_affected_ids(&conn, cutoff_timestamp)?;
        let rows_deleted = delete_old_events(&conn, cutoff_timestamp)?;

        if let Some(sender) = event_sender {
            emit_deleted_events(&message_ids, &sender);
        }
        info!(
            count = rows_deleted,
            ids = %message_ids.join(","),
            "persistence.processor_cleanup: deleted old events"
        );

        Ok(rows_deleted)
    }
}

// Local, private helpers to keep functions ≤30 lines and preserve behavior
fn fetch_affected_ids(conn: &Connection, cutoff_timestamp: i64) -> Result<Vec<String>> {
    let mut stmt = conn
        .prepare(
            "SELECT message_id FROM p2p_message_events WHERE processed = TRUE AND timestamp < ?1",
        )
        .with_context(|| "persistence.processor_cleanup: prepare select ids".to_string())?;
    let rows = stmt
        .query_map(rusqlite::params![cutoff_timestamp], |row| {
            row.get::<_, String>(0)
        })
        .with_context(|| "persistence.processor_cleanup: execute select ids".to_string())?;
    let mut ids = Vec::new();
    for row in rows {
        ids.push(row.with_context(|| "persistence.processor_cleanup: map id row".to_string())?);
    }
    Ok(ids)
}

fn delete_old_events(conn: &Connection, cutoff_timestamp: i64) -> Result<u32> {
    let rows_deleted = conn
        .execute(
            "DELETE FROM p2p_message_events WHERE processed = TRUE AND timestamp < ?1",
            rusqlite::params![cutoff_timestamp],
        )
        .with_context(|| "persistence.processor_cleanup: delete old events".to_string())?
        as u32;
    Ok(rows_deleted)
}

fn emit_deleted_events(ids: &[String], sender: &mpsc::UnboundedSender<MessageEvent>) {
    for id_str in ids {
        if let Ok(mid) = MessageId::from_str(id_str) {
            let _ = sender.send(MessageEvent::MessageFailed {
                message_id: mid,
                error: "Deleted by cleanup".to_string(),
            });
        }
    }
}
