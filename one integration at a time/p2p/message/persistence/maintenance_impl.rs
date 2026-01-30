use anyhow::Result;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;
use tokio::sync::mpsc;

// Import specialized modules for hyper-modular maintenance operations
use super::maintenance_event_processing::MaintenanceEventProcessing;
use super::maintenance_event_querying::MaintenanceEventQuerying;
use super::maintenance_statistics::MaintenanceStatisticsHandler;

/// Implementation maintenance for event processing and statistics operations
#[derive(Clone)]
pub struct MaintenanceImplCore {
    pub connection_pool: Arc<Pool<SqliteConnectionManager>>,
    pub stats_handler: MaintenanceStatisticsHandler,
}

impl MaintenanceImplCore {
    /// Create new maintenance implementation core
    pub fn new(connection_pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        let stats_handler = MaintenanceStatisticsHandler::new(connection_pool.clone());
        Self {
            connection_pool,
            stats_handler,
        }
    }

    /// Set event sender for emit operations
    pub fn with_event_sender(
        mut self,
        sender: mpsc::UnboundedSender<crate::p2p::P2PEvent>,
    ) -> Self {
        self.stats_handler = self.stats_handler.with_event_sender(sender);
        self
    }

    /// Get unprocessed events for external processing
    pub async fn get_unprocessed_events(
        &self,
        limit: Option<u32>,
    ) -> Result<Vec<super::events_core::PersistenceEvent>> {
        MaintenanceEventQuerying::get_unprocessed_events(self.connection_pool.clone(), limit).await
    }

    /// Mark events as processed
    pub async fn mark_events_processed(
        &self,
        message_ids: &[crate::p2p::message::types::MessageId],
    ) -> Result<()> {
        MaintenanceEventProcessing::mark_events_processed(self.connection_pool.clone(), message_ids)
            .await
    }

    /// Get detailed maintenance statistics with event emission
    pub async fn get_maintenance_statistics(
        &self,
    ) -> Result<super::maintenance_core::MaintenanceStatistics> {
        self.stats_handler.get_maintenance_statistics().await
    }

    /// Get event processing statistics
    pub async fn get_event_processing_stats(
        &self,
    ) -> Result<super::statistics_types::EventProcessingStats> {
        self.stats_handler.get_event_processing_stats().await
    }
}
