use anyhow::{Context, Result};
use libp2p::PeerId;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;

use super::events_core::PersistenceEvent;
use crate::p2p::message::types::MessageId;
use crate::p2p::MessageEvent;

// Import modular maintenance components
pub use super::maintenance_core::{
    MaintenanceCoreImpl, MaintenanceResult, MaintenanceStatistics, PersistenceHealth,
};
use super::maintenance_impl::MaintenanceImplCore;

/// Service maintenance implementation for database cleanup and health monitoring
#[derive(Clone)]
pub struct ServiceMaintenanceImpl {
    core: MaintenanceCoreImpl,
    implementation: MaintenanceImplCore,
}

impl ServiceMaintenanceImpl {
    /// Create new service maintenance implementation
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self {
            core: MaintenanceCoreImpl::new(pool.clone()),
            implementation: MaintenanceImplCore::new(pool),
        }
    }

    /// Cleanup old events and optimize database
    pub async fn maintenance_cleanup(&self, older_than_days: u32) -> Result<MaintenanceResult> {
        self.core.maintenance_cleanup(older_than_days).await
    }

    /// Health check for persistence service
    pub async fn health_check(&self) -> Result<PersistenceHealth> {
        self.core.health_check().await
    }

    /// Get unprocessed events for external processing
    pub async fn get_unprocessed_events(
        &self,
        limit: Option<u32>,
    ) -> Result<Vec<PersistenceEvent>> {
        self.implementation.get_unprocessed_events(limit).await
    }

    /// Mark events as processed
    pub async fn mark_events_processed(&self, message_ids: &[MessageId]) -> Result<()> {
        self.implementation.mark_events_processed(message_ids).await
    }

    /// Get detailed maintenance statistics
    pub async fn get_maintenance_statistics(&self) -> Result<MaintenanceStatistics> {
        self.implementation.get_maintenance_statistics().await
    }

    /// Process maintenance events using MessageEvent integration
    pub async fn process_maintenance_events(&self) -> Result<Vec<MessageEvent>> {
        let unprocessed = self
            .get_unprocessed_events(Some(100))
            .await
            .context("Failed to get unprocessed events for maintenance processing")?;

        let mut message_events = Vec::new();

        for event in unprocessed {
            let message_event = MessageEvent::MessageReceived {
                from: event.peer_id.unwrap_or_else(|| PeerId::random()),
                message: crate::p2p::message::types::P2PMessage::Chat {
                    id: event.message_id,
                    text: format!("Maintenance event: {:?}", event.event_type),
                    timestamp: chrono::Utc::now(),
                    reply_to: None,
                },
            };
            message_events.push(message_event);
        }

        Ok(message_events)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_maintenance_result_creation() {
        let result = MaintenanceResult::new(50, true);

        assert_eq!(result.events_cleaned, 50);
        assert!(result.database_optimized);
        assert!(result.is_successful());
        assert_eq!(result.total_processed(), 50);
    }

    #[test]
    fn test_persistence_health_creation() {
        let health = PersistenceHealth::new(true, 10, 5, 100);

        assert!(health.database_healthy);
        assert_eq!(health.total_connections, 10);
        assert_eq!(health.idle_connections, 5);
        assert_eq!(health.unprocessed_events, 100);
        assert!(health.is_healthy());
        assert_eq!(health.connection_utilization(), 50.0);
        assert!(!health.is_connection_stressed());
    }

    #[test]
    fn test_maintenance_statistics() {
        let stats = MaintenanceStatistics {
            database_size_bytes: 50 * 1024 * 1024, // 50MB
            total_messages: 1000,
            total_events: 5000,
            last_vacuum: None,
        };

        assert_eq!(stats.database_size_mb(), 50.0);
        assert!(!stats.needs_maintenance()); // Under 100MB threshold
    }
}
