use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;
use tokio::sync::mpsc;

use super::connection::ConnectionUtils;
use super::events_core::{PersistenceEvent, PersistenceEventType};
use crate::p2p::message::types::MessageId;
use crate::p2p::MessageEvent;

// Import modular processor components
use super::processor_core::ProcessorCoreImpl;
use super::processor_database::ProcessorDatabaseImpl;

/// Event processor implementation for MessageEvent integration and persistence tracking
#[derive(Clone)]
pub struct EventProcessorImpl {
    core: ProcessorCoreImpl,
    database: ProcessorDatabaseImpl,
}

impl EventProcessorImpl {
    /// Create new event processor with database and event channel
    pub fn new(
        pool: Arc<Pool<SqliteConnectionManager>>,
        event_sender: mpsc::UnboundedSender<MessageEvent>,
    ) -> Self {
        Self {
            core: ProcessorCoreImpl::new(pool.clone(), event_sender),
            database: ProcessorDatabaseImpl::new(pool),
        }
    }
    /// Process and store message event in database
    pub async fn process_message_event(&self, event: &MessageEvent) -> Result<()> {
        self.database
            .process_message_event(event)
            .await
            .with_context(|| "persistence.events_processor: process_message_event".to_string())
    }

    /// Emit persistence event to message event system
    pub async fn emit_persistence_event(&self, persistence_event: PersistenceEvent) -> Result<()> {
        let (_total, _idle) = ConnectionUtils::get_pool_stats(self.core.pool());
        match persistence_event.event_type {
            PersistenceEventType::DeliveryStatusUpdated => self
                .core
                .emit_persistence_event(persistence_event)
                .await
                .with_context(|| {
                    "persistence.events_processor: emit delivery_status_updated".to_string()
                }),
            PersistenceEventType::MessageStored
            | PersistenceEventType::MessageRetrieved
            | PersistenceEventType::MessageDeleted
            | PersistenceEventType::SearchPerformed => self
                .core
                .emit_persistence_event(persistence_event)
                .await
                .with_context(|| {
                    "persistence.events_processor: emit persistence_event".to_string()
                }),
        }
    }

    /// Get unprocessed events from database
    pub async fn get_unprocessed_events(&self, limit: Option<u32>) -> Result<Vec<MessageEvent>> {
        let persistence_events = self.database.get_unprocessed_events(limit).await?;
        let message_events = persistence_events
            .into_iter()
            .map(|pe| self.core.convert_persistence_to_message_event(&pe))
            .collect();
        Ok(message_events)
    }

    /// Mark events as processed in database
    pub async fn mark_events_processed(&self, message_ids: &[MessageId]) -> Result<()> {
        self.database.mark_events_processed(message_ids).await
    }

    /// Clean up old processed events
    pub async fn cleanup_old_events(&self, older_than_days: u32) -> Result<u32> {
        self.database.cleanup_old_events(older_than_days).await
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::p2p::message::persistence::{ConnectionManager, SchemaManager};
    use libp2p::PeerId;
    use tempfile::tempdir;

    #[tokio::test]
    async fn test_event_processor_creation() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());

        let (tx, _rx) = mpsc::unbounded_channel();
        let _processor = EventProcessorImpl::new(pool, tx);

        // Test passes if no panic occurs during creation
    }
}
