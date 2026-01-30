pub mod connection;
pub mod events;
pub mod operations;
pub mod queries;
pub mod schema;

// Helper modules
pub mod events_core;
pub mod events_processor;
pub mod events_statistics;
pub mod helpers_delivery;
pub mod helpers_message;
pub mod maintenance_core;
pub mod maintenance_event_processing;
pub mod maintenance_event_querying;
pub mod maintenance_impl;
pub mod maintenance_statistics;
pub mod operations_core;
pub mod operations_core_helpers;
pub mod operations_helpers;
pub mod operations_impl;
pub mod operations_impl_helpers;
pub mod operations_updater;
pub mod operations_verification;
pub mod processor_cleanup;
pub mod queries_analytics;
pub mod queries_basic;
pub mod queries_conversation;
pub mod queries_delivery;
pub mod queries_delivery_helpers;
pub mod queries_delivery_stats;
pub mod queries_helpers;
pub mod queries_search;
pub mod schema_fts;
pub mod schema_indexes;
pub mod schema_tables;

pub mod fts_core;
pub mod fts_maintenance;
pub mod statistics_impl;
pub mod statistics_types;

// Processor modules
pub mod processor_core;
pub mod processor_database;

// Import modular service components
mod service_core;
mod service_delegates;
mod service_maintenance;
mod service_operations;
mod service_operations_helpers;

pub use connection::*;
pub use events::*;
pub use operations::*;
pub use queries::*;
pub use schema::*;

// Re-export Task 3.5 query modules
pub use queries_conversation::ConversationQueries;
pub use queries_delivery::{DeliveryInfo, DeliveryQueries};
pub use queries_delivery_stats::{DeliveryStatistics, DeliveryStatisticsQueries};

// Re-export processor types
pub use processor_core::*;
pub use processor_database::*;

// Re-export service types for API compatibility
pub use service_core::PersistenceService;
pub use service_maintenance::{MaintenanceResult, PersistenceHealth, ServiceMaintenanceImpl};

#[cfg(test)]
mod tests {
    use super::*;
    use crate::p2p::MessageConfig;
    use tempfile::tempdir;
    use tokio::sync::mpsc;

    #[tokio::test]
    async fn test_persistence_service_creation() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");

        let config = MessageConfig {
            database_path: db_path.to_string_lossy().to_string(),
            ..Default::default()
        };

        let (tx, _rx) = mpsc::unbounded_channel();
        let service = PersistenceService::new(&config, tx).await.unwrap();

        let health = service.health_check().await.unwrap();
        assert!(health.database_healthy);
    }
}
pub mod operations_status;
