use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;
use tokio::sync::mpsc;

use crate::p2p::message::types::MessageId;
use crate::p2p::MessageEvent;

// Import modular components
use super::events_processor::EventProcessorImpl;
use super::events_statistics::EventStatisticsImpl;

// Re-export public types for API compatibility
pub use super::events_core::{PersistenceEvent, PersistenceEventType};
pub use super::events_statistics::EventStatistics;

/// Event processor for MessageEvent integration and persistence tracking
#[derive(Clone)]
pub struct EventProcessor {
    processor: EventProcessorImpl,
    statistics: EventStatisticsImpl,
}

impl EventProcessor {
    /// Create new event processor with database and event channel
    pub fn new(
        pool: Arc<Pool<SqliteConnectionManager>>,
        event_sender: mpsc::UnboundedSender<MessageEvent>,
    ) -> Self {
        Self {
            processor: EventProcessorImpl::new(pool.clone(), event_sender),
            statistics: EventStatisticsImpl::new(pool),
        }
    }

    /// Process and store message event in database
    pub async fn process_message_event(&self, event: &MessageEvent) -> Result<()> {
        self.processor
            .process_message_event(event)
            .await
            .with_context(|| {
                format!(
                    "persistence.events: process_message_event event={:?}",
                    event
                )
            })
    }

    /// Emit persistence event to message event system
    pub async fn emit_persistence_event(&self, persistence_event: PersistenceEvent) -> Result<()> {
        self.processor
            .emit_persistence_event(persistence_event)
            .await
            .with_context(|| "persistence.events: emit_persistence_event".to_string())
    }

    /// Get unprocessed events from database
    pub async fn get_unprocessed_events(&self, limit: Option<u32>) -> Result<Vec<MessageEvent>> {
        self.processor
            .get_unprocessed_events(limit)
            .await
            .with_context(|| {
                format!(
                    "persistence.events: get_unprocessed_events limit={:?}",
                    limit
                )
            })
    }

    /// Mark events as processed in database
    pub async fn mark_events_processed(&self, message_ids: &[MessageId]) -> Result<()> {
        self.processor
            .mark_events_processed(message_ids)
            .await
            .with_context(|| {
                format!(
                    "persistence.events: mark_events_processed count={}",
                    message_ids.len()
                )
            })
    }

    /// Clean up old processed events
    pub async fn cleanup_old_events(&self, older_than_days: u32) -> Result<u32> {
        self.processor
            .cleanup_old_events(older_than_days)
            .await
            .with_context(|| {
                format!(
                    "persistence.events: cleanup_old_events older_than_days={}",
                    older_than_days
                )
            })
    }

    /// Get event statistics for monitoring
    pub async fn get_event_statistics(&self) -> Result<EventStatistics> {
        self.statistics
            .get_event_statistics()
            .await
            .with_context(|| "persistence.events: get_event_statistics".to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::p2p::message::persistence::{ConnectionManager, SchemaManager};
    use tempfile::tempdir;

    use libp2p::PeerId;

    #[tokio::test]
    async fn test_event_processing() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());

        SchemaManager::initialize_schema(&pool).unwrap();

        let (tx, _rx) = mpsc::unbounded_channel();
        let processor = EventProcessor::new(pool, tx);

        let event = MessageEvent::MessageSent {
            to: PeerId::random(),
            message_id: MessageId::new_v4(),
        };

        processor.process_message_event(&event).await.unwrap();

        let stats = processor.get_event_statistics().await.unwrap();
        assert_eq!(stats.total_events, 1);
    }
}
