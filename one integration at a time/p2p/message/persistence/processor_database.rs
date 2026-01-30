use super::connection::ConnectionUtils;
use super::events_core::{PersistenceEvent, PersistenceEventType};
use super::processor_cleanup::ProcessorCleanup;
use crate::p2p::message::types::MessageId;
use crate::p2p::MessageEvent;
use anyhow::{Context, Result};
use libp2p::PeerId;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::{params, Connection};
use std::str::FromStr;
use std::sync::Arc;
use uuid;
/// Database processor implementation for event storage and retrieval
#[derive(Clone)]
pub struct ProcessorDatabaseImpl {
    pool: Arc<Pool<SqliteConnectionManager>>,
    cleanup: ProcessorCleanup,
}
impl ProcessorDatabaseImpl {
    /// Create new processor database
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        let cleanup = ProcessorCleanup::new(pool.clone());
        Self { pool, cleanup }
    }
    /// Convert MessageEvent to PersistenceEvent for database storage
    fn convert_message_event_to_persistence(
        &self,
        event: &MessageEvent,
    ) -> Result<PersistenceEvent> {
        let timestamp = chrono::Utc::now().timestamp();
        let (event_type, message_id, peer_id, metadata) = match event {
            MessageEvent::MessageSent { to, message_id } => (
                PersistenceEventType::MessageStored,
                *message_id,
                Some(*to),
                Some("Message sent".to_string()),
            ),
            MessageEvent::MessageReceived { from, message } => {
                let msg_id = message.message_id().unwrap_or_else(|| uuid::Uuid::new_v4());
                (
                    PersistenceEventType::MessageRetrieved,
                    msg_id,
                    Some(*from),
                    Some("Message received".to_string()),
                )
            }
            MessageEvent::MessageDelivered { message_id } => (
                PersistenceEventType::DeliveryStatusUpdated,
                *message_id,
                None,
                Some("Message delivered".to_string()),
            ),
            MessageEvent::MessageFailed { message_id, error } => (
                PersistenceEventType::MessageDeleted,
                *message_id,
                None,
                Some(error.clone()),
            ),
        };
        Ok(PersistenceEvent::new(
            event_type, message_id, peer_id, timestamp, metadata,
        ))
    }

    /// Process and store message event in database
    pub async fn process_message_event(&self, event: &MessageEvent) -> Result<()> {
        // Convert MessageEvent to PersistenceEvent for database storage
        let persistence_event = self.convert_message_event_to_persistence(event)?;

        let pool = self.pool.clone();

        tokio::task::spawn_blocking(move || {
            let mut conn = pool.get().context("Failed to get database connection")?;

            ConnectionUtils::execute_transaction(&mut conn, |tx| {
                Self::store_persistence_event(tx, &persistence_event)
            })
        })
        .await
        .context("Task join error")?
    }

    /// Get unprocessed events from database
    pub async fn get_unprocessed_events(
        &self,
        limit: Option<u32>,
    ) -> Result<Vec<PersistenceEvent>> {
        let pool = self.pool.clone();
        let limit = limit.unwrap_or(100);

        let result = tokio::task::spawn_blocking(move || {
            Self::execute_unprocessed_events_query(pool, limit)
        })
        .await
        .context("Task join error")?;

        result
    }

    /// Execute unprocessed events query
    fn execute_unprocessed_events_query(
        pool: Arc<r2d2::Pool<r2d2_sqlite::SqliteConnectionManager>>,
        limit: u32,
    ) -> Result<Vec<PersistenceEvent>> {
        let conn = pool.get().context("Failed to get database connection")?;

        let mut stmt = conn
            .prepare(
                "SELECT message_id, event_type, event_data, peer_id, timestamp
             FROM p2p_message_events
             WHERE processed = FALSE
             ORDER BY timestamp ASC
             LIMIT ?1",
            )
            .context("Failed to prepare unprocessed events query")?;

        let event_iter = stmt
            .query_map(params![limit], |row| Self::map_persistence_event_row(row))
            .context("Failed to execute unprocessed events query")?;

        Self::collect_persistence_event_results(event_iter)
    }

    /// Map database row to PersistenceEvent
    fn map_persistence_event_row(row: &rusqlite::Row) -> rusqlite::Result<PersistenceEvent> {
        let message_id = MessageId::from_str(&row.get::<_, String>(0)?).map_err(|_| {
            rusqlite::Error::InvalidColumnType(
                0,
                "message_id".to_string(),
                rusqlite::types::Type::Text,
            )
        })?;
        let event_type = Self::parse_persistence_event_type(&row.get::<_, String>(1)?);
        let peer_id = Self::parse_peer_id_optional(row.get::<_, Option<String>>(3)?)?;

        Ok(PersistenceEvent::new(
            event_type,
            message_id,
            peer_id,
            row.get(4)?,
            row.get(2)?,
        ))
    }

    /// Parse persistence event type from string
    fn parse_persistence_event_type(event_type_str: &str) -> PersistenceEventType {
        match event_type_str {
            "message_stored" => PersistenceEventType::MessageStored,
            "message_retrieved" => PersistenceEventType::MessageRetrieved,
            "delivery_status_updated" => PersistenceEventType::DeliveryStatusUpdated,
            "message_deleted" => PersistenceEventType::MessageDeleted,
            "search_performed" => PersistenceEventType::SearchPerformed,
            _ => PersistenceEventType::MessageStored,
        }
    }

    /// Parse optional peer ID from string
    fn parse_peer_id_optional(peer_id_str: Option<String>) -> rusqlite::Result<Option<PeerId>> {
        peer_id_str
            .map(|s| {
                s.parse::<PeerId>().map_err(|_| {
                    rusqlite::Error::InvalidColumnType(
                        3,
                        "peer_id".to_string(),
                        rusqlite::types::Type::Text,
                    )
                })
            })
            .transpose()
    }

    /// Collect persistence event results into vector
    fn collect_persistence_event_results<F>(
        event_iter: rusqlite::MappedRows<F>,
    ) -> Result<Vec<PersistenceEvent>>
    where
        F: FnMut(&rusqlite::Row) -> rusqlite::Result<PersistenceEvent>,
    {
        let mut events = Vec::new();
        for event_result in event_iter {
            events.push(event_result?);
        }
        Ok(events)
    }
    /// Mark events as processed in database
    pub async fn mark_events_processed(&self, message_ids: &[MessageId]) -> Result<()> {
        let pool = self.pool.clone();
        let message_ids: Vec<String> = message_ids.iter().map(|id| id.to_string()).collect();

        tokio::task::spawn_blocking(move || {
            let mut conn = pool.get().context("Failed to get database connection")?;

            ConnectionUtils::execute_transaction(&mut conn, |tx| {
                for message_id in &message_ids {
                    tx.execute(
                        "UPDATE p2p_message_events 
                         SET processed = TRUE, updated_at = unixepoch()
                         WHERE message_id = ?1",
                        params![message_id],
                    )
                    .context("Failed to mark event as processed")?;
                }
                Ok(())
            })
        })
        .await
        .context("Task join error")?
    }

    /// Store persistence event in database
    fn store_persistence_event(conn: &Connection, event: &PersistenceEvent) -> Result<()> {
        let event_type_str = match event.event_type {
            PersistenceEventType::MessageStored => "message_stored",
            PersistenceEventType::MessageRetrieved => "message_retrieved",
            PersistenceEventType::DeliveryStatusUpdated => "delivery_status_updated",
            PersistenceEventType::MessageDeleted => "message_deleted",
            PersistenceEventType::SearchPerformed => "search_performed",
        };

        conn.execute(
            "INSERT INTO p2p_message_events (
                message_id, event_type, event_data, peer_id, timestamp
            ) VALUES (?1, ?2, ?3, ?4, ?5)",
            params![
                event.message_id.to_string(),
                event_type_str,
                event.metadata,
                event.peer_id.as_ref().map(|p| p.to_string()),
                event.timestamp
            ],
        )
        .context("Failed to store persistence event")?;
        Ok(())
    }
    /// Clean up old events from database
    pub async fn cleanup_old_events(&self, older_than_days: u32) -> Result<u32> {
        self.cleanup.cleanup_old_events(older_than_days).await
    }
}
