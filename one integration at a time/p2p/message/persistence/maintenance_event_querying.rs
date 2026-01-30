use anyhow::Result;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;

/// Event querying functionality for maintenance operations
#[derive(Clone)]
pub struct MaintenanceEventQuerying;

impl MaintenanceEventQuerying {
    /// Get unprocessed events for external processing
    pub async fn get_unprocessed_events(
        connection_pool: Arc<Pool<SqliteConnectionManager>>,
        limit: Option<u32>,
    ) -> Result<Vec<super::events_core::PersistenceEvent>> {
        let pool = connection_pool.clone();
        let limit = limit.unwrap_or(100);
        let result = tokio::task::spawn_blocking(move || {
            Self::execute_unprocessed_events_query(pool, limit)
        })
        .await
        .map_err(|e| anyhow::anyhow!("Task join error: {}", e))??;
        Ok(result)
    }

    /// Execute unprocessed events query
    fn execute_unprocessed_events_query(
        pool: Arc<Pool<SqliteConnectionManager>>,
        limit: u32,
    ) -> Result<Vec<super::events_core::PersistenceEvent>> {
        let conn = pool
            .get()
            .map_err(|e| anyhow::anyhow!("Failed to get database connection: {}", e))?;
        let mut stmt = conn.prepare("SELECT message_id, event_type, peer_id, timestamp, metadata FROM p2p_message_events WHERE processed = FALSE ORDER BY timestamp ASC LIMIT ?1")?;
        let event_iter = stmt.query_map([limit], |row| Self::map_maintenance_event_row(row))?;
        Self::collect_maintenance_events(event_iter)
    }

    /// Map database row to PersistenceEvent for maintenance
    fn map_maintenance_event_row(
        row: &rusqlite::Row,
    ) -> rusqlite::Result<super::events_core::PersistenceEvent> {
        use super::events_core::PersistenceEventType;
        use std::str::FromStr;
        let message_id_str: String = row.get(0)?;
        let event_type: String = row.get(1)?;
        let peer_id_str: Option<String> = row.get(2)?;
        let timestamp: i64 = row.get(3)?;
        let metadata: Option<String> = row.get(4)?;
        let event_type = match event_type.as_str() {
            "message_stored" => PersistenceEventType::MessageStored,
            "message_retrieved" => PersistenceEventType::MessageRetrieved,
            "delivery_status_updated" => PersistenceEventType::DeliveryStatusUpdated,
            "message_deleted" => PersistenceEventType::MessageDeleted,
            "search_performed" => PersistenceEventType::SearchPerformed,
            _ => PersistenceEventType::MessageStored,
        };
        Ok(super::events_core::PersistenceEvent::new(
            event_type,
            crate::p2p::message::types::MessageId::from_str(&message_id_str)
                .unwrap_or_else(|_| crate::p2p::message::types::MessageId::new_v4()),
            peer_id_str.and_then(|s| s.parse().ok()),
            timestamp,
            metadata,
        ))
    }

    /// Collect maintenance event results
    fn collect_maintenance_events<F>(
        event_iter: rusqlite::MappedRows<F>,
    ) -> Result<Vec<super::events_core::PersistenceEvent>>
    where
        F: FnMut(&rusqlite::Row) -> rusqlite::Result<super::events_core::PersistenceEvent>,
    {
        let mut events = Vec::new();
        for event_result in event_iter {
            events.push(event_result?);
        }
        Ok(events)
    }
}
